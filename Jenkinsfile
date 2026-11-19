
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code checkout completed'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'py -3.12 -m venv .venv-ci'
                bat '.venv-ci\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Automated Tests') {
            steps {
                bat '.venv-ci\\Scripts\\python -m pytest tests/ -v'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t campus-platform:%BUILD_NUMBER% .'
            }
        }
    }

    post {
        success {
            echo 'CampusPlatform pipeline completed successfully'
        }
        failure {
            echo 'CampusPlatform pipeline failed'
        }
    }
}
