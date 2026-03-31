pipeline {
    agent none 
    
    stages {
        stage('Backend: Test & Verify') {
            agent { 
                docker { image 'python:3.11-alpine' } 
            }
            steps {
                // Navigate into the backend directory
                dir('backend') {
                    sh 'pip install -r requirements.txt'
                    // In a real scenario, you run pytest here
                    sh 'python -m py_compile app.py' 
                    echo "Backend compilation verified."
                }
            }
        }
        
        stage('Frontend: Build Artifacts') {
            agent { 
                docker { image 'node:20-alpine' } 
            }
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build' // This creates the 'dist' folder
                }
            }
        }

        stage('Publish Artifacts') {
            agent any
            steps {
                // This is the answer to "where is my app"
                // This saves the frontend build output directly into Jenkins UI
                archiveArtifacts artifacts: 'frontend/dist/**', allowEmptyArchive: false
                echo "React build saved. You can download it from the Jenkins Build page."
            }
        }
    }
}