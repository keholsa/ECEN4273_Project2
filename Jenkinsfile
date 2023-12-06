pipeline {
    agent any
    

    }
    stages {
        stage('Checkout'){
            steps{
               checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/keholsa/ECEN4273_Project2.git']])
            }
        }
          
        stage('Establishing virtual env'){
            steps{
                script{
                sh 'python3 -m venv venv'
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

    

