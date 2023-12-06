pipeline {
    agent {

    docker {
        image 'python:3' 
           }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
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

