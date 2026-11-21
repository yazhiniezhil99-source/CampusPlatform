
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
                bat '.venv-ci\\Scripts\\python -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                bat '"C:/Users/manib/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe" build -t campus-platform:%BUILD_NUMBER% .'
            }
        }

        stage('AWS Deployment') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'campusplatform-ec2-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    bat '"C:/Windows/System32/OpenSSH/ssh.exe" -i "%SSH_KEY%" -o StrictHostKeyChecking=accept-new %SSH_USER%@51.21.161.11 "cd ~/CampusPlatform && git pull origin main && docker build -t campus-platform:latest . && (docker rm -f campus-platform-container >/dev/null 2>&1 || true) && docker run -d --name campus-platform-container --restart unless-stopped -p 80:8000 campus-platform:latest"'
                }
            }
        }
    }

    post {
        success {
            echo 'CampusPlatform CI/CD pipeline completed successfully'
        }
        failure {
            echo 'CampusPlatform pipeline failed'
        }
    }
}
