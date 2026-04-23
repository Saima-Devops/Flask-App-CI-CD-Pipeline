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

**RUn Pytest on local:**

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

### 1. Create an EC2 Instance with:

- Ubuntu 22.04
- Open ports:
- 22 (SSH)
- 80 (HTTP)

-------

### 2. Install dependencies on EC2

```bash
sudo apt update -y
sudo apt install -y python3-pip python3-venv nginx git
```

-------

### 3. Create application directory

```bash
sudo mkdir -p /var/www/flask-app

sudo chown -R ubuntu:ubuntu /var/www/flask-app
```
----


## STEP-5 Now Create Workflow Folder for github Actions

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


---------------

## STEP-8: 







-----




#### Project Structure for Jenkins Pipeline

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



------












## Author 

Saima Usman
PPMCAD-15

---

## License

MIT License

---
