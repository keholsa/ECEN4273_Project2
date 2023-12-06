pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Add Dependancies'){
            steps{
                sh 'pipx install pygame'
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh 'python3 project2cpu.py'
                }
            }
        }
    }
}
