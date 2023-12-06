pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

    stage('Establishing virtual env'){
        steps{
            script{
                sh 'python3 -m venv venv'
                sh 'venv/bin/activate'
            }
        }
    }

        stage('Dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Build') {
            steps {
                sh 'python3 project2.py'
            }
        }
    }
}
