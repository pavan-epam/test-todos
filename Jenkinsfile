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
                    echo "Backend compilation verified."
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

        stage('Publish Artifacts') {
            agent any
            steps {
                // This saves the 'dist' folder to the Jenkins Master
                archiveArtifacts artifacts: 'frontend/dist/**', allowEmptyArchive: false
                echo "Success! You can find your compiled React files in the Artifacts section of this build."
            }
        }
    }
    
    post {
        always {
            // Good practice to clean up the workspace on the EC2 host
            cleanWs()
        }
    }
}
