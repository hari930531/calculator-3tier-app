# 3-Tier Calculator Web Application on AWS EC2 with CloudWatch & SNS Monitoring

An end-to-end production deployment of a containerized 3-tier web application (Frontend, Backend, and MySQL Database) on an AWS EC2 instance. This project includes automated infrastructure health monitoring using Amazon CloudWatch alarms, email notification delivery through Amazon SNS, validation via CPU stress testing, and cost-preventative teardown.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Project Directory Structure](#project-directory-structure)
- [1. Launching the AWS EC2 Instance](#1-launching-the-aws-ec2-instance)
- [2. Host Provisioning & Command Reference](#2-host-provisioning--command-reference)
- [3. Application Deployment via Docker Compose](#3-application-deployment-via-docker-compose)
- [4. Database Persistence Verification](#4-database-persistence-verification)
- [5. Setting Up CloudWatch Alarms & SNS Alerting](#5-setting-up-cloudwatch-alarms--sns-alerting)
- [6. CPU Stress Testing & Telemetry Validation](#6-cpu-stress-testing--telemetry-validation)
- [7. Complete Resource Teardown (Zero-Cost Cleanup)](#7-complete-resource-teardown-zero-cost-cleanup)
- [Troubleshooting & Verification](#troubleshooting--verification)

---

## Architecture Overview

```text
[ Client Web Browser ]
         │ (HTTP Port 80)
         ▼
[ Tier 1: Frontend (Nginx Container) ]
         │ (Internal / Port 5000)
         ▼
[ Tier 2: Application Backend (Flask / Node.js API) ]
         │ (Internal / Port 3306)
         ▼
[ Tier 3: Database (MySQL Container) ]
         │
         ├── Stores calculation records in 'calculator_db.calculations'
         └── Persistent volume mounted on EC2 host storage

[ AWS Infrastructure Observability ]
   EC2 (calculator-server) ──(CPUUtilization ≥ 80%)──► CloudWatch Alarm ──► SNS Topic ──► Alert Email
```

---

## Prerequisites

- An active **AWS Account** (Free Tier eligible).
- Basic familiarity with Linux shell commands and SSH.
- An email address to receive SNS alert notifications.

---

## Project Directory Structure

```text
calculator-3tier-app/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── style.css
│   └── app.js
├── backend/
│   ├── Dockerfile
│   ├── app.py (or server.js)
│   └── requirements.txt (or package.json)
└── database/
    └── init.sql
```

---

## 1. Launching the AWS EC2 Instance

1. Navigate to the **AWS Management Console** → **EC2** → **Launch instance**.
2. Configure the following parameters:
   - **Name:** `calculator-server`
   - **AMI:** `Amazon Linux 2023 AMI` (or `Amazon Linux 2`)
   - **Architecture:** `64-bit (x86)`
   - **Instance Type:** `t2.micro` or `t3.micro` (Free Tier eligible)
   - **Key Pair:** Select an existing key pair or use **EC2 Instance Connect**.
   - **Network Settings:**
     - **Auto-assign Public IP:** `Enable`
     - **Security Group Inbound Rules:**
       - **SSH (22):** `0.0.0.0/0` (or `My IP`)
       - **HTTP (80):** `0.0.0.0/0`
       - **Custom TCP (5000):** `0.0.0.0/0` (Backend API)
       - **MySQL (3306):** `0.0.0.0/0` (or restricted to VPC CIDR)
   - **Storage:** Default `8 GiB gp3` root volume.
3. Click **Launch instance** and wait for the status to show **Running** with **2/2 checks passed**.

---

## 2. Host Provisioning & Command Reference

Connect to the instance via **EC2 Instance Connect** or SSH and run the following setup commands:

### Update the OS Packages
```bash
sudo dnf update -y
```
- **Explanation:** Updates system repository metadata and installs patches. `-y` automatically confirms installation prompts. (Use `sudo yum update -y` if using Amazon Linux 2).

### Install Docker and Git
```bash
sudo dnf install docker git -y
```
- **Explanation:** Installs the Docker containerization runtime engine and Git version control utility.

### Start and Enable the Docker Daemon
```bash
sudo systemctl start docker
sudo systemctl enable docker
```
- **Explanation:** `start` immediately triggers the background Docker service daemon. `enable` configures Docker to automatically start on instance reboot.

### Grant Non-Root Docker Privileges
```bash
sudo usermod -aG docker ec2-user
newgrp docker
```
- **Explanation:** `usermod -aG` appends the `ec2-user` to the `docker` administrative group so you can run containers without prefixing `sudo`. `newgrp docker` activates group changes in the current session.

---

## 3. Application Deployment via Docker Compose

### Clone the Repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd calculator-3tier-app
```

### Start the Multi-Container Stack
```bash
docker compose up -d --build
```
- **Explanation:** 
  - `--build`: Builds Docker images locally from the respective `Dockerfile` definitions.
  - `-d`: Runs the containers in background "detached" mode, freeing up your terminal.

### Verify Running Containers
```bash
docker ps
```
- **Explanation:** Displays container IDs, status, exposed ports, and names. You should see 3 running containers: Frontend (`80:80`), Backend (`5000:5000`), and MySQL (`3306:3306`).

Access the application in your browser:
```text
http://<YOUR_EC2_PUBLIC_IP>
```

---

## 4. Database Persistence Verification

To verify that calculations submitted in the frontend are successfully persisted into MySQL:

### Log into the Database Container
```bash
docker exec -it <MYSQL_CONTAINER_NAME_OR_ID> mysql -u root -p
```
*(Or log in directly if using a local MySQL client: `mysql -u root -p`)*

### Inspect Application Data
```sql
-- View all databases
SHOW DATABASES;

-- Switch to the application database
USE calculator_db;

-- Confirm table creation
SHOW TABLES;

-- Inspect stored calculation transactions
SELECT * FROM calculations;

-- Exit MySQL shell
exit;
```

---

## 5. Setting Up CloudWatch Alarms & SNS Alerting

### Step 5.1: Create Amazon SNS Topic & Email Subscription
1. Open the **Amazon SNS Console** → **Topics** → **Create topic**.
2. Type: **Standard** | Name: `Default_CloudWatch_Alarms_Topic`. Click **Create topic**.
3. Inside the topic page, click **Create subscription**.
4. Protocol: **Email** | Endpoint: your email address (e.g., `hari930531@gmail.com`). Click **Create subscription**.
5. **Critical Step:** Open your email inbox, find the confirmation email from AWS, and click **Confirm subscription**. The subscription status will switch from *Pending Confirmation* to *Confirmed*.

### Step 5.2: Create CloudWatch Alarm
1. Open the **Amazon CloudWatch Console** → **Alarms** → **Create alarm**.
2. Click **Select metric** → **EC2** → **Per-Instance Metrics**.
3. Select metric `CPUUtilization` for your `calculator-server` instance.
4. Set the following conditions:
   - **Statistic:** `Average`
   - **Period:** `5 minutes` (300 seconds)
   - **Threshold type:** `Static`
   - **Condition:** `Greater/Equal (>= 80.0%)`
5. Under **Configure actions**:
   - Alarm state trigger: `In alarm`
   - Send notification to: `Default_CloudWatch_Alarms_Topic`
6. Enter Alarm Name: `Default_CloudWatch_Alarms_Topic` and click **Create alarm**.
7. Initially, the alarm status will evaluate to **OK**.

---

## 6. CPU Stress Testing & Telemetry Validation

Simulate heavy CPU workloads to ensure the telemetry pipeline triggers an alert email:

### Install the Stress Package
```bash
# For Amazon Linux 2023:
sudo dnf install stress -y

# For Amazon Linux 2:
# sudo amazon-linux-extras install epel -y && sudo yum install stress -y
```

### Trigger 100% CPU Load
```bash
stress --cpu 2 --timeout 360s
```
- **Explanation:**
  - `--cpu 2`: Dispatches 2 worker processes running compute-heavy `sqrt()` loops, maxing out CPU utilization.
  - `--timeout 360s`: Enforces automatic process termination after 360 seconds (6 minutes) to prevent accidental infinite load.

### Observed Results
1. **Terminal:** Displays `stress: info: [47798] dispatching hogs: 2 cpu...` and concludes after 360 seconds.
2. **CloudWatch Alarm:** CPU usage spikes past 80% (typically ~84-85%), transitioning state from **OK** to **In alarm**.
3. **Email Notification:** AWS SNS dispatches an alert email:
   - **Subject:** `ALARM: "Default_CloudWatch_Alarms_Topic" in Asia Pacific (Hyderabad)`
   - **Details:** Includes threshold cross metrics and exact datapoint values.
4. **Auto-Recovery:** Once the timeout completes, CPU utilization drops and the alarm automatically transitions back to **OK**.

---

## 7. Complete Resource Teardown (Zero-Cost Cleanup)

To eliminate any chance of ongoing AWS charges from compute hours, public IPv4 addresses, or provisioned EBS storage, delete resources in the following order:

### 1. Delete Amazon SNS Topic
- Open **Amazon SNS** → **Topics**.
- Select `Default_CloudWatch_Alarms_Topic` → click **Delete**.
- Confirm deletion by typing `delete me`.
- (Optional) Navigate to **Subscriptions** and delete any orphan subscriptions.

### 2. Delete CloudWatch Alarm
- Open **CloudWatch** → **Alarms**.
- Select `Default_CloudWatch_Alarms_Topic`.
- Click **Actions** → **Delete** and confirm.

### 3. Terminate EC2 Instance
- Open **EC2 Console** → **Instances**.
- Select `calculator-server`.
- Click **Instance state** → **Terminate instance**.
- Confirm termination.
- **Note:** The attached root EBS storage volume (`gp3`) has `DeleteOnTermination` enabled by default and will be automatically deallocated, preventing storage fees.

---

## Troubleshooting & Verification

| Issue | Root Cause | Resolution |
| :--- | :--- | :--- |
| **Cannot access Web UI via browser** | Security Group missing Port 80 / Port 5000 | Add an inbound rule in EC2 Security Groups for Port 80/5000 with source `0.0.0.0/0`. |
| **SNS email not received** | Subscription unconfirmed or stuck in Spam | Check Spam/Junk folder and verify that the confirmation link in the initial AWS email was clicked. |
| **Alarm stuck in "Insufficient Data"** | Not enough metrics collected yet | Wait 5 to 10 minutes or generate load with `stress` so CloudWatch can sample data points. |
| **Cannot delete attached EBS volume** | Volume is `in-use` by EC2 instance | You do not need to delete it manually; terminating the EC2 instance automatically terminates attached root storage. |