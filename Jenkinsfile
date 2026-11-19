
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
                bat '"C:/Users/manib/AppData/Local/Programs/Python/Python312/python.exe" -m venv .venv-ci'
                bat '.venv-ci\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Automated Tests') {
            steps {
                bat '"C:/Users/manib/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe" build -t campus-platform:3 .'
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
