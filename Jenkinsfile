pipeline {
    agent any

    options {
        skipDefaultCheckout()
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout & Fix Ownership') {
            steps {
                // Fix for Git "dubious ownership" error when Jenkins runs in Docker
                sh 'git config --global --add safe.directory "*"'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('backend') {
                    // Using bat instead of sh since OS is windows, but let's check if they were using sh before.
                    // Yes, they were using 'sh'. I'll stick to 'sh' if they are using Git Bash or WSL inside Jenkins, 
                    // but if it's Windows, usually 'bat' is used. I'll keep 'sh' as it was already there.
                    sh 'docker build -t task-app .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                // Stop and remove existing container if it exists, to avoid port conflicts on automated runs
                sh 'docker stop task-app-container || true'
                sh 'docker rm task-app-container || true'
                sh 'docker run -d --name task-app-container -p 5000:5000 task-app'
            }
        }
    }
}