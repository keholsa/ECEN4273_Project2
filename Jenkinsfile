pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Add Dependencies'){
            steps{
                sh 'pip install numpy --break-system-packages'
                sh 'pip install pygame --break-system-packages'
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh 'python3 project2cpu.py'
                    sh 'python3 project2cpu_gui.py'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest --verbose'
                }
            }
        }

        stage('Deployment'){
            steps{
                script{

                    // enable docker commands in jenkins
                     // sh 'docker build -t project2cd .'
                     // sh 'docker run -it project2cd'
                     }
                }
            }
    }
}
