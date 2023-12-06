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
                    // Assuming your Python files are in the root of the project
                    sh 'python3 project2cpu.py'
                    sh 'python3 project2cpu_gui.py'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                   for (int i = 1; i <= 100; i++) {
                        echo "Running iteration ${i}"
                        sh 'python3 project2cpu.py'
                    }
                }
            }
        }

        // stage('Deployment') {
        //     steps {
        //         script {
        //             // Uncomment the following lines if you want to build and run a Docker container
        //             // sh 'docker build -t project2cd .'
        //             // sh 'docker run -it project2cd'
        //         }
        //     }
        // }
    }

    post {
        success {
            echo 'All stages passed! Deployment complete...'
            // You can add additional steps or notifications here
        }
    }
}
