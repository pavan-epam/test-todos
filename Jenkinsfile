pipeline {
    agent none 
    
    stages {
        stage('Backend: Test & Verify') {
            agent { 
                docker { 
                    image 'python:3.11-alpine'
                    args '-u root'
                } 
            }
            steps {
                dir('backend') {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                    sh 'python -m py_compile app.py' 
                }
            }
        }
        
        stage('Frontend: Build Artifacts') {
            agent { 
                docker { 
                    image 'node:20-alpine'
                    args '-u root' 
                } 
            }
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build' 
                }
            }
        }

        stage('Publish Artifacts to Jenkins') {
            agent any
            steps {
                archiveArtifacts artifacts: 'frontend/dist/**', allowEmptyArchive: false
            }
        }

        stage('Build & Push to DockerHub') {
            agent any
            environment {
                DOCKER_USER = 'pavanepam'
            }
            steps {
                // Injects the credentials securely
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'CREDS_USER')]) {
                    // Login to DockerHub
                    sh "echo \$DOCKER_PASS | docker login -u \$CREDS_USER --password-stdin"

                    // 1. Build and Push Backend
                    dir('backend') {
                        sh "docker build -t ${DOCKER_USER}/test-todos-backend:latest ."
                        sh "docker push ${DOCKER_USER}/test-todos-backend:latest"
                    }

                    // 2. Build and Push Frontend
                    dir('frontend') {
                        sh "docker build -t ${DOCKER_USER}/test-todos-frontend:latest ."
                        sh "docker push ${DOCKER_USER}/test-todos-frontend:latest"
                    }
                    
                    // Cleanup local images to save EC2 disk space
                    sh "docker rmi ${DOCKER_USER}/test-todos-backend:latest"
                    sh "docker rmi ${DOCKER_USER}/test-todos-frontend:latest"
                }
            }
        }

        stage('Deploy to Kubernetes (CD)') {
            agent any 
            environment {
                // Forces kubectl to use the Minikube cluster config owned by the Jenkins user
                KUBECONFIG = '/var/lib/jenkins/.kube/config'
            }
            steps {
                echo "Deploying applications to Minikube..."
                
                sh "kubectl apply -f k8s/backend.yaml"
                sh "kubectl apply -f k8s/frontend.yaml"
                
                sh "kubectl rollout restart deployment/backend-deploy"
                sh "kubectl rollout restart deployment/frontend-deploy"
                
                echo "Deployment triggered successfully!"
            }
        }
    }
}
