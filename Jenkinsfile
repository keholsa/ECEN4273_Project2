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
                sh 'pipx install random'
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
