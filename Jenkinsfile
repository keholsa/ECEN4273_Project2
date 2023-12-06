pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Establishing Virtual Environment') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                }
            }
        }
        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                script {
                    // Activate the virtual environment and install dependencies
                    bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests or Build') {
            steps {
                script {
                    // Execute your tests or build commands here
                    bat 'venv\\Scripts\\activate.bat && python your_script.py'
                }
            }
        }
    }
}

