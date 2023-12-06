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
                    sh 'venv\\Scripts\\activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests or Build') {
            steps {
                script {
                    // Execute your tests or build commands here
                    sh 'venv\\Scripts\\activate && python your_script.py'
                }
            }
        }

    }
}

