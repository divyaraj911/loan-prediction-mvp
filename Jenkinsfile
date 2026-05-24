// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Source Control Checkout') {
            steps {
                echo 'Pulling fresh repository codebase snapshots directly from GitHub...'
                checkout scm
            }
        }

        stage('Static Code Quality Check') {
            steps {
                echo 'Verifying Python source script syntax integrity...'
                sh 'python3 -m py_compile src/app.py src/train.py'
                echo 'Syntax integrity: VALID.'
            }
        }

        stage('Automated Model Validation') {
            steps {
                echo 'Executing standalone machine learning execution tests...'
                sh 'python3 src/train.py'
                echo 'Model pipeline evaluation completed successfully!'
            }
        }
    }

    post {
        success {
            echo 'CI/CD execution passed completely. Codebase build is production ready!'
        }
    }
}