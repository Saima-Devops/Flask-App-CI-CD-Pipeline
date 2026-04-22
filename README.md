# Flask App CI/CD Pipeline in 2 ways


## PART 1 —  CI/CD through GitHub Actions


### Step-01: Fork the Source Code from Github Repo

- Source Code Repo Link  ---> Fork  --->  My own Repo Name  ---> Fork only the main branch
-  Click Fork
- Clone it locally:

 ```bash 
git clone https://github.com/Saima-Devops/Flask-App-CI-CD-Pipeline.git
cd Flask-App-CI-CD-Pipeline
````
-----

### Step-02: Run & Test the App Locally

#### Project Structure 

```bash
flask-app/
│── app.py
│── requirements.txt
│── .env
│── templates/
│── .github/workflows/deploy.yml
│── start_flask.sh
│── test_app.py
│── Jenkinsfile
```

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

### Local Setup

#### Create a Virtual Environment first

```bash
python -m venv venv
# Activate venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate
```

#### Install all dependencies

```bash
pip install -r requirements.txt
python3 app.py
```

<img width="1314" height="647" alt="image" src="https://github.com/user-attachments/assets/ecdd5405-ae5c-4674-9ca0-7665b52d3898" />

-----

#### Run the App locally

<img width="1919" height="595" alt="image" src="https://github.com/user-attachments/assets/16f2772f-77b1-4342-9b23-3f142ff27ea5" />


**Check its functionality**

<img width="1908" height="652" alt="image" src="https://github.com/user-attachments/assets/3daa6f12-cfbb-4280-a7bd-3e19688209ae" />

**Everything is working fine** 👍

----

**Ran Pytest on local:**

<img width="1570" height="413" alt="image" src="https://github.com/user-attachments/assets/02910f77-e641-4952-a117-172783ce94f1" />


------

### Step-03: Github Branching Setup

#### Create Branches

```bash
git checkout -b staging
git push origin staging
git checkout main
```

<img width="1290" height="525" alt="image" src="https://github.com/user-attachments/assets/4a3f46fb-fda5-478b-a6ef-6dc03998c0b3" />


<img width="1864" height="797" alt="image" src="https://github.com/user-attachments/assets/c8822567-567c-4bc0-87b3-f211466cca7c" />

---

### Step-04: Now Create Workflow Folder for github Actions

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

### Step 5: Add Secrets (Required)

**Go to Github Repo:**

`Repo → Settings → Secrets → Actions`

**Add:**

- **DEPLOY_KEY**
- **API_TOKEN**
- **MONGO_URI**
- **STAGING_HOST**
- **STAGING_USER**
- **STAGING_SSH_KEY**


<img width="1887" height="755" alt="image" src="https://github.com/user-attachments/assets/acff3e42-135a-41b8-ac09-0c4690cf6587" />

----------

### Deployment Flow

- Push to staging branch
- GitHub Actions runs CI
- Deploys to EC2
- Restarts Flask service
- Nginx serves app

---------------

### Step 6: Push Code to Github

```bash
git add .
git commit -m "Added GitHub Actions CI/CD pipeline"
git push origin main
```

**This triggers:**

- Install dependencies
- Run tests
- Build

<img width="1887" height="778" alt="image" src="https://github.com/user-attachments/assets/0c1d4021-21a2-4001-9857-cd0bfbb26cda" />












## Author 

Saima Usman
PPMCAD-15

---

## License

MIT License

---
