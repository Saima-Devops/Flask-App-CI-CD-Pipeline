# Flask App CI/CD Pipeline in 2 ways (with Github Actions & Jenkins)


## PART 1 — Flask CI/CD Pipeline (GitHub Actions + EC2 Staging Deployment)

### Project Overview

This project demonstrates a complete CI/CD pipeline for a Flask web application using:

- GitHub Actions for Continuous Integration (CI)
- Automated testing (pytest)
- Code quality checks (pylint, bandit)
- Deployment to an AWS EC2 staging environment using SSH

-----

### Tech Stack

- **Python 3.10** → Core programming language for application development
- **Flask** → Web framework used to build the application’s backend services
- **MongoDB** → NoSQL database used for storing and managing data 
- **GitHub Actions** → CI/CD platform used to automate testing and deployment workflows
- **EC2** → AWS Ubuntu Server for Staging Environment
- **Gunicorn** → Production-grade WSGI server used to run the Flask application
- **Nginx** → Reverse proxy server used to handle client requests and forward them to Gunicorn 
- **systemd** → Service manager used to run and manage the Flask application as a background service

-----

### Repository Structure

```bash
flask_Practice/
│
├── app.py
├── requirements.txt
├── test_app.py
├── .github/
│   └── workflows/
│       └── ci-cd.yaml
├── templates/
├── static/
└── README.md
```
----

### CI/CD Pipeline Architecture

```bash
GitHub Push (staging branch)
        ↓
GitHub Actions Trigger
        ↓
CI Job (Test + Lint + Security Scan)
        ↓
If Success → SSH into EC2
        ↓
Pull latest code
        ↓
Install dependencies
        ↓
Restart Flask service (systemd)
        ↓
Nginx serves application
```

----

### CONTINUOUS INTEGRATION (CI)

✔ Runs automatically on every push to:
- `staging`

#### CI Steps:

- Checkout repository
- Setup Python environment
- Install dependencies
- Run linting (pylint)
- Run security scan (bandit)
- Execute test suite (pytest)

-----

#### CI Tools Used

- pytest → unit testing
- pylint → code quality check
- bandit → security analysis

-------

### HOW TO RUN TESTS LOCALLY

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v
```
------

#### First Things First 

## STEP-1: Fork the Source Code from Github Repo

- Source Code Repo Link  ---> Fork  --->  My own Repo Name  ---> Fork only the main branch
-  Click Fork
- Clone it locally:

 ```bash 
git clone https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git
cd Flask-App-CI-CD-Pipeline
````
-----

## STEP-2: Run & Test the App Locally

Open the project folder in 'VSCode'

<img width="1891" height="993" alt="image" src="https://github.com/user-attachments/assets/d056f3b9-471c-4e81-aaab-3f260303b07a" />

-----

### Connect with MongoDB and get the URI 

<img width="1474" height="726" alt="image" src="https://github.com/user-attachments/assets/c6d1c612-a446-4e80-953d-47c9ea8806ee" />


### Set Environment Variables

Create `.env` file:

```bash
MONGO_URI=<your mongodb_connection_string_here>
```
-----

## Local Setup

### Create a Virtual Environment first

```bash
python -m venv venv
# Activate venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate
```

### Install all dependencies

```bash
pip install -r requirements.txt
python3 app.py
```

<img width="1314" height="647" alt="image" src="https://github.com/user-attachments/assets/ecdd5405-ae5c-4674-9ca0-7665b52d3898" />

-----

### Run the App locally

<img width="1919" height="595" alt="image" src="https://github.com/user-attachments/assets/16f2772f-77b1-4342-9b23-3f142ff27ea5" />


**Check its functionality**

<img width="1908" height="652" alt="image" src="https://github.com/user-attachments/assets/3daa6f12-cfbb-4280-a7bd-3e19688209ae" />

**Everything is working fine** 👍

----

**Run Pytest on local:**

<img width="1570" height="413" alt="image" src="https://github.com/user-attachments/assets/02910f77-e641-4952-a117-172783ce94f1" />


------

## CONTINUOUS DEPLOYMENT (CD) - STAGING ON EC2

Deployment happens only when code is pushed to:

`staging branch`


## STEP-3 Github Branching Setup

```bash
git checkout -b staging
git push origin staging
git checkout main
```

<img width="1290" height="525" alt="image" src="https://github.com/user-attachments/assets/4a3f46fb-fda5-478b-a6ef-6dc03998c0b3" />


<img width="1864" height="797" alt="image" src="https://github.com/user-attachments/assets/c8822567-567c-4bc0-87b3-f211466cca7c" />

-----

## STEP-4 AWS EC2 STAGING ENVIRONMENT SETUP

### Create an EC2 Instance with:

- Ubuntu 22.04
- Open ports:
- 22 (SSH)
- 80 (HTTP)

-------

### Install dependencies on EC2

```bash
sudo apt update -y
sudo apt install -y python3-pip python3-venv nginx git
```

-------

### Create application directory

```bash
sudo mkdir -p /var/www/flask-app

sudo chown -R ubuntu:ubuntu /var/www/flask-app
```
----

### Gunicorn Setup

```
pip install gunicorn
gunicorn -w 3 -b 127.0.0.1:5000 app:app
```
---

### Systemd Service

Create file:

```
sudo nano /etc/systemd/system/flask-app.service
```

### Service Config

```
[Unit]
Description=Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/flask-app
Environment="PATH=/var/www/flask-app/venv/bin"
ExecStart=/var/www/flask-app/venv/bin/gunicorn -w 3 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Start Service

```
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
```

<img width="1229" height="572" alt="1" src="https://github.com/user-attachments/assets/33ab6015-80a2-42a4-a6cc-9bbcae2d85f5" />


---

### Nginx Configuration

```
sudo nano /etc/nginx/sites-available/flask-app
```

### Config

```
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Enable

```
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled

sudo nginx -t
sudo systemctl restart nginx
```

<img width="1240" height="382" alt="3" src="https://github.com/user-attachments/assets/c536f84c-8a69-4dfb-9965-a28693280177" />



----


## STEP-5 Now Create Workflow Folder for GitHub Actions

**Create Folders:**

```bash
.github/workflows/
````
Create `ci-cd.yaml` inside folders as: `.github/workflows/ci-cd.yaml`


**nano `ci-cd.yaml`**

```bash
name: Flask CI/CD Pipeline

on:
  push:
    branches: [master, staging]

permissions:
  contents: read

jobs:

# ----------- CI -----------
  ci:
    runs-on: ubuntu-latest

    services:
      mongo:
        image: mongo:6
        ports:
          - 27017:27017

    env:
      MONGO_URI: mongodb://localhost:27017/testdb

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install & Test
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt pytest pylint bandit

          pylint app.py || true
          bandit -r . -s B104,B101
          pytest -v


# ----------- STAGING -----------
  deploy-staging:
    needs: ci
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest

    steps:
      - uses: webfactory/ssh-agent@v0.7.0
        with:
          ssh-private-key: ${{ secrets.STAGING_SSH_KEY }}

      - name: Deploy Staging
        env:
          MONGO_URI: ${{ secrets.MONGO_URI }}
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.STAGING_USER }}@${{ secrets.STAGING_HOST }} \
          "MONGO_URI='${MONGO_URI}' bash -s" << EOF
          set -e

          APP_DIR="/var/www/flask-app"
          echo "🚀 Staging Deploy"

          sudo rm -rf \$APP_DIR
          sudo mkdir -p \$APP_DIR
          sudo chown -R \$USER:\$USER \$APP_DIR
          cd \$APP_DIR

          git clone -b staging https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git .

          echo "MONGO_URI=\$MONGO_URI" > .env

          sudo apt update -y
          sudo apt install -y python3-venv python3-pip nginx

          python3 -m venv venv
          source venv/bin/activate

          pip install --upgrade pip
          pip install -r requirements.txt
          pip install gunicorn

          sudo systemctl daemon-reload
          sudo systemctl enable flask-app
          sudo systemctl restart flask-app

          sudo systemctl restart nginx

          echo "✅ Staging Done"
          EOF


# ----------- PRODUCTION -----------
  deploy-production:
    needs: ci
    if: github.ref == 'refs/heads/master'
    runs-on: ubuntu-latest

    steps:
      - uses: webfactory/ssh-agent@v0.7.0
        with:
          ssh-private-key: ${{ secrets.PROD_SSH_KEY }}

      - name: Deploy Production
        env:
          MONGO_URI: ${{ secrets.MONGO_URI }}
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.PROD_USER }}@${{ secrets.PROD_HOST }} \
          "MONGO_URI='${MONGO_URI}' bash -s" << EOF
          set -e

          APP_DIR="/var/www/flask-app"
          echo "🚀 Production Deploy"

          sudo rm -rf \$APP_DIR
          sudo mkdir -p \$APP_DIR
          sudo chown -R \$USER:\$USER \$APP_DIR
          cd \$APP_DIR

          git clone -b master https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git .

          echo "MONGO_URI=\$MONGO_URI" > .env

          sudo apt update -y
          sudo apt install -y python3-venv python3-pip nginx

          python3 -m venv venv
          source venv/bin/activate

          pip install --upgrade pip
          pip install -r requirements.txt
          pip install gunicorn

          sudo systemctl daemon-reload
          sudo systemctl enable flask-app
          sudo systemctl restart flask-app

          sudo systemctl restart nginx

          echo "✅ Production Done!"
          EOF
```

<img width="1914" height="941" alt="image" src="https://github.com/user-attachments/assets/3220c151-b275-4c6f-89d7-180e8f1f8ef1" />

-----

## STEP-6: Add Github Secrets (Required)

**Go to Github Repo:**

`Repo → Settings → Secrets → Actions`

**Add:**

- **MONGO_URI**
- **STAGING_HOST** = (EC2 public ip)
- **STAGING_USER** = (ec2 username, ubuntu in my case)
- **STAGING_SSH_KEY** = (.pem file)


<img width="1854" height="433" alt="image" src="https://github.com/user-attachments/assets/1f097660-959b-458c-a0a8-ba6d0dd906d9" />


----------

### Deployment Flow

- Push to staging branch
- GitHub Actions runs CI
- Deploys to EC2
- Restarts Flask service
- Nginx serves the app

---------------

## STEP-7: Push Code to Github from the Staging Branch

```bash
git add .
git commit -m "Added GitHub Actions CI/CD pipeline"
git push origin staging
```

**This triggers:**

- Install dependencies
- Run tests
- Build

<img width="1887" height="778" alt="image" src="https://github.com/user-attachments/assets/0c1d4021-21a2-4001-9857-cd0bfbb26cda" />

<img width="1887" height="523" alt="6" src="https://github.com/user-attachments/assets/86b0e842-dd6c-471f-8b2e-b5fc376a037f" />

<img width="1891" height="939" alt="image" src="https://github.com/user-attachments/assets/73e9b7e6-ecf7-47e2-98e3-7f02afeff282" />

----------

## What This Pipeline Does

- `main` :  Runs CI only (test, lint, security)
- `staging` :  Runs CI + deploys to EC2

<img width="1915" height="907" alt="image" src="https://github.com/user-attachments/assets/05515009-3657-41b9-b13a-eaadc3f11a45" />

---

## STEP-8: Access the App

```bash
http://<EC2-PUBLIC-IP>
```

<img width="1911" height="869" alt="12" src="https://github.com/user-attachments/assets/8c52dbdf-a9ec-4562-9597-ea3e580ce57d" />

<img width="1919" height="522" alt="8" src="https://github.com/user-attachments/assets/c424d89d-1241-4900-a6a2-2e161cc166f7" />

<img width="1919" height="547" alt="9" src="https://github.com/user-attachments/assets/43627edd-756c-4519-a94b-2d27abf86823" />

<br>

### Final Output
✔ CI/CD fully automated\
✔ Flask app deployed\
✔ Nginx reverse proxy working

------

## PART:2 CI/CD Pipeline Automation with Jenkins

### Stages

- Install Dependencies
- Lint & Security (pylint + bandit)
- Run Tests (pytest)
- Deploy Staging (branch: staging)

-----

### Project Structure for Jenkins Pipeline

```bash
flask-app/
│── app.py
│── requirements.txt
│── .env
│── templates/
│── .github/workflows/ci-cd.yml
│── start_flask.sh
│── test_app.py
│── Jenkinsfile
```


-----

### Jenkins Credentials

| ID          | Type        |
|-------------|------------ |
| staging-ssh | SSH Key     |
| MONGO_URI   | Secret Text |
| STAGING_IP  | Secret Text |


----

### Github Webhook

<img width="1912" height="946" alt="image" src="https://github.com/user-attachments/assets/72e86378-63d3-419f-823b-76ff7bac8284" />

----

### Create Jenkinsfile

```groovy

pipeline {
    agent any

    environment {
        MONGO_URI = credentials('MONGO_URI')
        EC2_HOST = '54.221.90.160'
        EC2_USER = 'ubuntu'
        APP_DIR  = '/home/ubuntu/flask-app'
    }

    options {
        timestamps()
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
                set -e
                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt

                # Dev tools
                pip install pytest pylint bandit
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                set -e
                . venv/bin/activate

                echo "🔍 Running pylint..."
                pylint app.py || true

                echo "🔐 Running bandit (only scanning app code)..."
                bandit app.py -s B104,B101
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                set -e
                . venv/bin/activate
                pytest -v
                '''
            }
        }

        stage('Deploy to EC2 (Staging)') {
            steps {
                sshagent(['ec2-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST '
                        set -e

                        echo "🚀 Starting Deployment"

                        if [ -d "$APP_DIR/.git" ]; then
                            cd $APP_DIR
                            git fetch origin
                            git reset --hard origin/staging
                        else
                            git clone -b staging https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git $APP_DIR
                            cd $APP_DIR
                        fi

                        echo "📦 Setting ENV"
                        echo "MONGO_URI=$MONGO_URI" > .env

                        echo "🐍 Setting up Python env"
                        python3 -m venv venv
                        source venv/bin/activate

                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install gunicorn

                        echo "🔄 Restarting services"
                        sudo systemctl daemon-reload
                        sudo systemctl restart flask-app
                        sudo systemctl restart nginx

                        echo "✅ Deployment Successful"
                    '
                    """
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

```

----

### Build Pipeline Now

<img width="1259" height="621" alt="Screenshot 2026-04-23 at 11 53 21 PM" src="https://github.com/user-attachments/assets/7a5cce3b-f13b-4a09-8e1a-30d7bb84d643" />

<img width="2524" height="1230" alt="image" src="https://github.com/user-attachments/assets/4f282a0e-9a0e-4a7a-8711-5ec35c7af339" />

<img width="902" height="663" alt="Screenshot 2026-04-24 at 12 17 18 AM" src="https://github.com/user-attachments/assets/264d1961-1830-4b8e-aad9-87fc022711b8" />

<img width="1918" height="947" alt="image" src="https://github.com/user-attachments/assets/c41cb063-f2f3-4106-9c7e-f482cda69871" />


<br>


🟢 Success after some troubleshooting!! 

Hurrey!! ✅🎉


------

## Troubleshooting

Fixed the Jenkinsfile Code Quality Stage as it was scanning the venv folder as well so I excluded that. Here's the change:

```groovy
stage("Code Quality") {
    steps {
        sh '''
        source .venv/bin/activate
        pylint app.py || true
        bandit -r . --exclude .venv
        '''
    }
}
```

<br>

✅ All Errors Fixed!!

------

## Author 

**Saima Usman**\
Jr. DevOps Engineer\
(PPMCAD-15 Hero-Vired)

---

## License

MIT License

---
