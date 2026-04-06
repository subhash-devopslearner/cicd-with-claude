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
                docker build -t cicd-django-project .
                '''
            }            
        }
        stage('Push docker image...') {
            steps {                
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    sh '''
                    echo $DOCKERHUB_PASSWORD | docker login --username=$DOCKERHUB_USERNAME --password-stdin                    
                    docker tag cicd-django-project $DOCKERHUB_USERNAME/cicd-django-project:latest
                    docker push $DOCKERHUB_USERNAME/cicd-django-project:latest
                    '''
                }               
            }
        }
        stage('Deploy staging...') {
            when {
                branch 'staging'
                //expression { env.GIT_BRANCH == 'origin/staging' }
            }
            steps {             
                echo 'Deploying to staging'
                withCredentials([file(credentialsId: 'CICD_PROJECT_STAGING_ENV_FILE', variable: 'STAGING_ENV_FILE')]) {
                    sh '''
                    cp $STAGING_ENV_FILE .env
                    docker compose -f docker-compose.yml -f docker-compose-staging.yml up -d --remove-orphans
                    '''
                } 
            }            
        }
        stage('Deploy production...') {
            when {
                branch 'main'
                //expression { env.GIT_BRANCH == 'origin/main' }
            }
            steps {                    
                echo 'Deploying to production'
                withCredentials([file(credentialsId: 'CICD_PROJECT_PRODUCTION_ENV_FILE', variable: 'PRODUCTION_ENV_FILE')]) {
                    sh '''
                    cp $PRODUCTION_ENV_FILE .env
                    docker compose -f docker-compose.yml -f docker-compose-production.yml up -d --remove-orphans
                    '''
                } 
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
        always {            
            sh '''
            echo 'Cleaning up...'     
            docker compose logs web || true       
            rm .env || true            
            '''
        }
    }
}