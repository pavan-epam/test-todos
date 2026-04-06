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

        // --- NEW SONARQUBE STAGE ---
        stage('SonarQube Code Analysis') {
            agent {
                docker { 
                    image 'sonarsource/sonar-scanner-cli:latest'
                    args '-u root'
                }
            }
            environment {
                // REPLACE with the IP of your new SonarQube EC2 instance
                SONAR_HOST_URL = 'http://54.242.157.218:9000'
            }
            steps {
                // Pulls the token you saved in Jenkins Credentials
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=test-todos \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_TOKEN} \
                        -Dsonar.exclusions=frontend/node_modules/**,frontend/dist/**
                    '''
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
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'CREDS_USER')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$CREDS_USER --password-stdin"

                    dir('backend') {
                        sh "docker build -t ${DOCKER_USER}/test-todos-backend:latest ."
                        sh "docker push ${DOCKER_USER}/test-todos-backend:latest"
                    }

                    dir('frontend') {
                        sh "docker build -t ${DOCKER_USER}/test-todos-frontend:latest ."
                        sh "docker push ${DOCKER_USER}/test-todos-frontend:latest"
                    }
                    
                    sh "docker rmi ${DOCKER_USER}/test-todos-backend:latest"
                    sh "docker rmi ${DOCKER_USER}/test-todos-frontend:latest"
                }
            }
        }

        /* =========================================================
        COMMENTED OUT: Deploy to Kubernetes (CD)
        We will return to this when the K8s infrastructure is ready.
        =========================================================
        
        stage('Deploy to Kubernetes (CD)') {
            agent any 
            environment {
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
        */
    }
}
