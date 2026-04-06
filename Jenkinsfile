pipeline {
    agent {
        label 'linux'
    }

    stages{        
        stage('Testing...') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                python cicdproject/manage.py test
                '''
            }            
        }
        stage('Build docker image...') {
            steps {
                echo 'Building docker image'
                sh '''
                docker build -t cicdproject .
                '''
            }            
        }
        stage('Deploy...') {
            steps {
                echo 'Deploying to staging'
            }            
        }
    }
    post {
        success {
            echo 'Pipeline successful'
        }
        failure {
            echo 'Pipeline failed'
        }        
    }
}