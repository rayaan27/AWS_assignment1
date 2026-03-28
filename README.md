# 🎓 UniEvent — University Event Management System on AWS
**CE 308/408 Cloud Computing — Assignment 1**  
**GIK Institute of Engineering Sciences and Technology**

---

## 📌 Project Overview
UniEvent is a cloud-hosted web application where students can browse university events. It automatically fetches real event data from the **Ticketmaster API** and stores event images in **AWS S3**. The system is deployed on **AWS EC2** instances inside private subnets, behind an **Application Load Balancer** for fault tolerance and scalability.

---

## 🏗️ AWS Architecture

```
User (Browser)
      ↓
Internet Gateway
      ↓
Application Load Balancer  ← Public Subnets (2 AZs)
      ↓           ↓
EC2 Instance 1  EC2 Instance 2  ← Private Subnets
      ↓
NAT Gateway → Ticketmaster API
      ↓
S3 Bucket (Event Images)
```

### AWS Services Used
| Service | Purpose |
|---------|---------|
| **IAM** | EC2 role with S3 access permissions |
| **VPC** | Isolated network with public & private subnets |
| **EC2** | Two Ubuntu instances running the Flask app |
| **S3** | Stores event poster images |
| **ALB** | Load balancer for traffic distribution & fault tolerance |

---

## 🔌 External API
**Ticketmaster Discovery API**  
- Provides: event title, date, venue, city, description, images  
- Format: JSON  
- Docs: https://developer.ticketmaster.com

---

## 📁 Project Structure
```
Assignment1_AWS_CE/
├── app.py                 # Flask app — fetches API, uploads to S3, serves web page
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Frontend HTML page
├── static/
│   └── style.css          # Styling
├── setup.sh               # EC2 installation script
└── README.md              # This file
```

---

## 🚀 Step-by-Step Deployment Guide

### Step 1 — Prerequisites
- AWS Account (free tier)
- Ticketmaster API Key from https://developer.ticketmaster.com
- GitHub Account

---

### Step 2 — Clone This Repository
```bash
git clone https://github.com/YOUR_USERNAME/Assignment1_AWS_CE.git
cd Assignment1_AWS_CE
```

---

### Step 3 — Configure Your Keys
Open `app.py` and replace:
```python
TICKETMASTER_API_KEY = "YOUR_TICKETMASTER_API_KEY"
S3_BUCKET_NAME       = "unievents-media-bucket-yourname"
AWS_REGION           = "us-east-1"
```

---

### Step 4 — AWS Setup (Console)

#### 4.1 IAM Role
1. Go to IAM → Roles → Create Role
2. Select: AWS Service → EC2
3. Attach policy: `AmazonS3FullAccess`
4. Name: `EC2-UniEvent-Role`

#### 4.2 VPC
1. Go to VPC → Create VPC → Select "VPC and more"
2. Name: `UniEvent-VPC`
3. CIDR: `10.0.0.0/16`
4. 2 public subnets + 2 private subnets + NAT Gateway

#### 4.3 S3 Bucket
1. Go to S3 → Create Bucket
2. Name: `unievents-media-bucket-yourname`
3. Uncheck "Block all public access"

#### 4.4 EC2 Instances
Launch 2 instances:
- OS: Ubuntu 22.04
- Type: t2.micro (free tier)
- Place in private subnets
- Attach IAM role: `EC2-UniEvent-Role`
- Key pair: `unievents-key`

#### 4.5 Application Load Balancer
1. Go to EC2 → Load Balancers → Create ALB
2. Name: `UniEvent-ALB`
3. Scheme: Internet-facing
4. Select both public subnets
5. Create target group with both EC2 instances
6. Copy the DNS name — this is your website URL

---

### Step 5 — Connect to EC2 and Run App

#### Connect via SSH
```bash
chmod 400 unievents-key.pem
ssh -i unievents-key.pem ubuntu@<EC2-PRIVATE-IP>
```

#### Run Setup Script
```bash
chmod +x setup.sh
sudo ./setup.sh
```

#### Or manually:
```bash
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/YOUR_USERNAME/Assignment1_AWS_CE.git
cd Assignment1_AWS_CE
pip3 install -r requirements.txt
sudo python3 app.py
```

---

### Step 6 — Access the Website
1. Go to AWS Console → EC2 → Load Balancers
2. Copy the **DNS name** of `UniEvent-ALB`
3. Open in browser:
```
http://UniEvent-ALB-XXXXXXX.us-east-1.elb.amazonaws.com
```

---

## 🔒 Security Design
- EC2 instances are in **private subnets** — not directly accessible from internet
- Only the Load Balancer is in the public subnet
- EC2 accesses S3 via **IAM role** — no hardcoded credentials
- NAT Gateway allows EC2 to make outbound API calls without being exposed

## ⚙️ Fault Tolerance
- Two EC2 instances in **different Availability Zones**
- Load Balancer performs **health checks** every 30 seconds
- If one EC2 fails, all traffic is automatically routed to the other

---

## 👨‍💻 Author
**GIK Institute — CE 308/408 Cloud Computing**  
Assignment 1 — Deployment of a Scalable University Event Management System on AWS
