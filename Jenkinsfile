pipeline {
    agent any{
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
                    // Create and activate a virtual environment
                    sh 'python -m venv venv'
                    def activateScript = isUnix() ? 'venv/bin/activate' : 'venv\\Scripts\\activate'
                    sh "source $activateScript"

                    // Install project dependencies
                    sh 'pip install -r requirements.txt'

                    // Run your Python script
                    sh 'python project2.py'
                }
            }
        }
    }
}
