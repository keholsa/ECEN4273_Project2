pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // stage('Add Dependancies'){
        //     steps{
        //         sh 'pipx install pygame'
        //     }
        // }
        
        stage('Build CPU w/o GUI') {
            steps {
                script {
                    sh 'python3 project2cpu.py'
                }
            }
        }

        stage('Build CPU w/ GUI'){
            steps{
                sh 'python3 project2cpu_gui.py'
            }
        }
    }
}
