pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'hari930531/calculator-backend'
        DOCKER_CRED     = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "===> Step 1: Checking out repository from Git..."
                checkout scm
            }
            post {
                success {
                    echo "[SUCCESS]: Stage 1 - Code checkout completed successfully."
                }
                failure {
                    echo "[FAILED]: Stage 1 - Code checkout failed."
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "===> Step 2: Building Backend Docker images..."
                dir('backend') {
                    // Build both build-number tagged image and latest tag
                    bat "docker build -t %DOCKER_HUB_REPO%:%BUILD_NUMBER% ."
                    bat "docker build -t %DOCKER_HUB_REPO%:latest ."
                }
            }
            post {
                success {
                    echo "[SUCCESS]: Stage 2 - Docker image build completed successfully."
                }
                failure {
                    echo "[FAILED]: Stage 2 - Docker image build failed."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "===> Step 3: Authenticating and pushing images to Docker Hub..."
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CRED}", 
                    usernameVariable: 'DOCKER_USERNAME', 
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    // Authenticate to Docker Hub
                    bat "docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%"
                    
                    // Push images
                    bat "docker push %DOCKER_HUB_REPO%:%BUILD_NUMBER%"
                    bat "docker push %DOCKER_HUB_REPO%:latest"
                }
            }
            post {
                success {
                    echo "[SUCCESS]: Stage 3 - Docker images pushed to Docker Hub successfully."
                }
                failure {
                    echo "[FAILED]: Stage 3 - Docker push failed."
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo "===> Step 4: Deploying full application stack using Docker Compose..."
                // Stop previous running containers and start updated stack
                bat "docker-compose down"
                bat "docker-compose up --build -d"
            }
            post {
                success {
                    echo "[SUCCESS]: Stage 4 - Application deployed successfully."
                }
                failure {
                    echo "[FAILED]: Stage 4 - Application deployment failed."
                }
            }
        }
    }

    post {
        always {
            echo "=================================================="
            echo "Pipeline run completed."
            echo "=================================================="
        }
        success {
            echo "[PIPELINE SUCCESS]: All pipeline stages passed successfully."
        }
        failure {
            echo "[PIPELINE FAILURE]: The build failed. Check console output for logs."
        }
    }
}