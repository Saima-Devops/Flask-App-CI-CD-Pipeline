pipeline {
    agent any

    environment {
        MONGO_URI = credentials('MONGO_URI')
        EC2_HOST = '54.221.90.160'
        EC2_USER = 'ubuntu'
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'staging', url: 'https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3.12 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest pylint bandit
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                . venv/bin/activate
                pylint app.py || true
                bandit -r . -s B104,B101
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest -v
                '''
            }
        }

        stage('Deploy to EC2 (Staging)') {
            steps {
                sshagent(['ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST << EOF
                    set -e

                    APP_DIR="/home/ubuntu/flask-app"

                    echo "🚀 Jenkins Staging Deploy"

                    if [ -d "$APP_DIR/.git" ]; then
                      cd $APP_DIR
                      git fetch origin
                      git reset --hard origin/staging
                    else
                      git clone -b staging https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git $APP_DIR
                      cd $APP_DIR
                    fi

                    echo "MONGO_URI=$MONGO_URI" > .env

                    python3 -m venv venv
                    source venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install gunicorn

                    sudo systemctl daemon-reload
                    sudo systemctl restart flask-app
                    sudo systemctl restart nginx

                    echo "✅ Deployment Done"
                    EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded'
        }
        failure {
            echo '❌ Pipeline failed'
        }
    }
}