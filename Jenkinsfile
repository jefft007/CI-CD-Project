pipeline {

    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/jefft007/CI-CD-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t task-app backend'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 5000:5000 task-app'
            }
        }

    }

}