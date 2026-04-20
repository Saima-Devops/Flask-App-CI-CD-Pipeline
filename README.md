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
MONGO_URI=mongodb+srv://saimausmandxb_db_user:U1-------@cluster.-----t.mongodb.net/students
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

<img width="1911" height="770" alt="image" src="https://github.com/user-attachments/assets/f05bd716-a8d3-4fb6-b709-628013f06d09" />

**Check its functionality**

<img width="1908" height="652" alt="image" src="https://github.com/user-attachments/assets/3daa6f12-cfbb-4280-a7bd-3e19688209ae" />


**Everything is working fine** 👍

------

### Step-03: Github Branching Setup

#### Create Branches

```bash
git checkout -b staging
git push origin staging
git checkout main
```


---

## Author 

Saima Usman
PPMCAD-15

---

## License

MIT License

---


