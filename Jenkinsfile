pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Import Library(s)'){
            steps{
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh 'python3 project2.py'
                }
            }
        }
    }
}
