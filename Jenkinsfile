pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "hari930531/calculator-backend"
        DOCKER_CRED     = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "===> Checking out code from GitHub..."
                checkout scm
            }
            post {
                success {
                    echo "✅ [SUCCESS]: Stage 1 - Code Checkout completed successfully!"
                }
                failure {
                    echo "❌ [FAILED]: Stage 1 - Code Checkout failed!"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "===> Building Docker images for Backend..."
                dir('backend') {
                    // Windows environment aana thala 'bat' use pandrom
                    bat "docker build -t %DOCKER_HUB_REPO%:%BUILD_NUMBER% ."
                    bat "docker build -t %DOCKER_HUB_REPO%:latest ."
                }
            }
            post {
                success {
                    echo "✅ [SUCCESS]: Stage 2 - Docker Image Build completed successfully!"
                }
                failure {
                    echo "❌ [FAILED]: Stage 2 - Docker Image Build failed!"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "===> Logging in to Docker Hub and pushing images..."
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CRED}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    bat "docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%"
                    bat "docker push %DOCKER_HUB_REPO%:%BUILD_NUMBER%"
                    bat "docker push %DOCKER_HUB_REPO%:latest"
                }
            }
            post {
                success {
                    echo "✅ [SUCCESS]: Stage 3 - Docker Images pushed to Docker Hub successfully!"
                }
                failure {
                    echo "❌ [FAILED]: Stage 3 - Docker Push failed!"
                }
            }
        }
    }

    // Full Pipeline mudiyumbothu varum status
    post {
        success {
            echo "=========================================================="
            echo "🎉 [ALL STAGES PASSED]: Pipeline executed successfully!"
            echo "=========================================================="
        }
        failure {
            echo "=========================================================="
            echo "⚠️ [PIPELINE FAILED]: Please check the console output errors."
            echo "=========================================================="
        }
    }
}