pipeline {
    agent any
    
    environment{
        PATH = "$PATH:C:/Program Files/CMake/bin"
    }
    stages {
        stage('Checkout'){
            steps{
               checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/keholsa/ECEN4273_Project2.git']])
            }
        }
        
        // stage('Install Python and Pip') {
        //     steps {
        //         script {
        //             sh 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
        //             sh 'python3 get-pip.py'
                    
        //             sh 'pip install --upgrade pip'
        //             sh 'pip install --upgrade setuptools'
        //         }
        //     }
        // }
        
        
        stage('Establishing virtual env'){
            steps{
                script{
                sh 'python -m venv venv'
                sh 'source venv/bin/activate'
            
                }
            }
        }
        stage('Dependencies'){
            steps{
                script{
                sh 'pip install -r requirements.txt'
        
                }
            }
        }
        
        stage('Build'){
            steps{
                sh 'python3 project2.py'    
            }
        }
    }
}
