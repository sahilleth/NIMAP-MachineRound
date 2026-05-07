pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'rohitpatil18/fastapi-app'
        DEPLOY_SERVER = '192.168.1.100'
        DEPLOY_USER = 'deploy'
        DEPLOY_PATH = '/opt/fastapi-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out from GitHub...'
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/RohitPatil18/docker-fastapi-test.git']]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image with tag: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                script {
                    sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .'
                    sh 'docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                            docker push ${DOCKER_IMAGE}:latest
                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                echo "Deploying to ${DEPLOY_SERVER}..."
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'deploy-server-ssh', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                        sh '''
                            ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} "mkdir -p ${DEPLOY_PATH}"
                            scp -i "$SSH_KEY" -o StrictHostKeyChecking=no docker-compose.yml ${DEPLOY_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}/
                            scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -r monitoring ${DEPLOY_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}/
                            ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_SERVER} "cd ${DEPLOY_PATH} && docker compose up -d"
                        '''
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                script {
                    sh '''
                        sleep 5
                        curl -f http://${DEPLOY_SERVER}:8000/ || exit 1
                        echo "Health check passed!"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
