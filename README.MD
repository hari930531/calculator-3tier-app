# 3-Tier Web Calculator Application

A complete production-ready three-tier web application built with a modern Frontend, Python Flask REST API Backend, and MySQL Database. The application is containerized using Docker, automated via a Jenkins CI/CD pipeline, deployed on AWS EC2, and monitored with Amazon CloudWatch.

---

## Architecture Overview

```text
[ Browser / Client ]
         │
         ▼ (Port 80)
┌─────────────────────────────────┐
│        Frontend (Nginx)         │
│     HTML5 / CSS3 / Vanilla JS   │
└─────────────────────────────────┘
         │
         ▼ (Port 5000: REST API)
┌─────────────────────────────────┐
│     Backend (Python / Flask)    │
│        Business Logic           │
└─────────────────────────────────┘
         │
         ▼ (Port 3306)
┌─────────────────────────────────┐
│       Database (MySQL 8.0)      │
│   Calculation History Storage   │
└─────────────────────────────────┘
Tech Stack
​Frontend: HTML5, CSS3, Vanilla JavaScript, Nginx (Alpine)
​Backend: Python 3.10, Flask, Flask-CORS, MySQL Connector
​Database: MySQL 8.0
​Containerization: Docker, Docker Compose
​CI/CD Automation: Jenkins Pipeline
​Cloud & Hosting: AWS EC2 (Ubuntu 22.04 LTS, Free-Tier t2.micro)
​Monitoring: Amazon CloudWatch (EC2 Basic Monitoring & Alarms)
​Registry: Docker Hub

**​Project Structure**

calculator-app/
├── frontend/
│   ├── index.html         # User interface
│   ├── style.css          # Responsive styling
│   └── script.js          # API calls and DOM manipulation
├── backend/
│   ├── app.py             # Flask application & database operations
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container definition
├── docker-compose.yml     # Multi-container orchestration
├── Jenkinsfile            # Automated CI/CD pipeline script
└── README.md              # Project documentation

Features
# ​Arithmetic Operations: Performs addition, subtraction, multiplication, and division.
# ​Persistent History: Stores every calculation with timestamps in MySQL.
# ​Resilient Database Handshake: Implements automated retry loops on backend startup to ensure MySQL readiness.
# ​Fully Containerized: Runs seamlessly across environments using isolated Docker networks and volumes.
# ​Automated Deployment: Jenkins automatically triggers on code pushes, builds images, pushes to Docker Hub, and executes rolling deployments on AWS EC2.
# ​Zero Infrastructure Cost: Designed entirely within the AWS Free Tier threshold.

**​Local Development Setup**
# ​Prerequisites
    ​Docker Desktop installed and running
    ​Git installed

**​StepS:**
    1.cLONE THE REPOSITORY:
    git clone [https://github.com/](https://github.com/)<your-username>/calculator-app.git
    cd calculator-app

    2.CONFIGURE API URL FOR LOCAL TESTIN:frontend/script.js
    const API_URL = "http://localhost:5000";

    3.START THE CONTAINERS:
    docker compose up -d --build

    4.VERIFY RUNNING CONTAINERS:
    docker ps

    5.ACCESS THE APPLICATION:
    FRONTEND: //localhost
    BACKEND Health/History:open
    http://localhost:5000/history

   **#  CI/CD Pipeline (Jenkins)**
​The pipeline automates deployment through the following stages:
# ​1.Checkout SCM: Clones the latest branch from GitHub.
# 2.​Build Docker Image: Builds and tags the Python backend image with the build number and latest.
# ​3.Push to Docker Hub: Authenticates using Jenkins credentials (dockerhub-credentials) and pushes the images.
# 4.​Deploy to EC2: SSH into the AWS EC2 instance, pulls the latest image, and restarts the services using docker compose.

# **​AWS Deployment & Monitoring**
​EC2 Security Group Rules
Type        Port    Protocol    Source      Description
SSH         22      TCP         Your IP     Secure Server Access
HTTP        80      TCP         0.0.0.0/0   Frontend UI
Custom TCP  5000    TCP         0.0.0.0/0   Backend API

# **Amazon CloudWatch Integration**
# ​1.Basic Monitoring: Default 5-minute metric collection for CPUUtilization, NetworkIn, NetworkOut, and DiskReadBytes.
# 2.​Metric Alarm: Configured to alert when CPUUtilization > 80% for 2 consecutive periods.
# ​3.SNS Notification: Triggers email alerts if server resource thresholds are breached

LICENSE
Distributed under the MIT License.