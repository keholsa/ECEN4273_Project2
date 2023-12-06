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
                    sh 'python -m venv venv'
                }
            }
        }

        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                script {
                    // Activate the virtual environment and install dependencies
                    sh 'source venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests or Build') {
            steps {
                script {
                    // Execute your tests or build commands here
                    sh 'source venv/bin/activate && python project2.py'
                }
            }
        }

    }
}

