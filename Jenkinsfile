pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "your_dockerhub_username/calculator-backend"
        DOCKER_CRED = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dir('backend') {
                        sh "docker build -t ${DOCKER_HUB_REPO}:${BUILD_NUMBER} ."
                        sh "docker build -t ${DOCKER_HUB_REPO}:latest ."
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CRED) {
                        sh "docker push ${DOCKER_HUB_REPO}:${BUILD_NUMBER}"
                        sh "docker push ${DOCKER_HUB_REPO}:latest"
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                // EC2-la Docker compose pull & up pannalam
                sshagent(['ec2-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@<EC2_PUBLIC_IP> "
                            cd /home/ubuntu/calculator-app &&
                            docker compose pull &&
                            docker compose up -d --remove-orphans
                        "
                    '''
                }
            }
        }
    }
}