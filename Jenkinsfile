// Jenkinsfile
pipeline {
    agent any

    environment {
        IMAGE_NAME = "loan-predictor-pipeline"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Source Control Checkout') {
            steps {
                echo 'Pulling fresh repository codebase snapshots directly from GitHub...'
                checkout scm
            }
        }

        stage('Container Image Compilation') {
            steps {
                echo 'Building optimized application layers and initializing internal training...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Liveness Integration Test') {
            steps {
                echo 'Spreading test container deployment instance to verify backend routing...'
                sh "docker run -d -p 8085:8000 --name pipeline_test_instance ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "sleep 5"
                // Run a simple network ping test against the application health probe
                sh "curl -f http://localhost:8085/health"
                echo 'Application health check passed successfully!'
                sh "docker rm -f pipeline_test_instance"
            }
        }
    }

    post {
        always {
            echo 'Pruning loose intermediate dangling image cache layers...'
            sh "docker image prune -f"
        }
        success {
            echo 'CI/CD execution passed completely. Codebase build is production ready!'
        }
    }
}