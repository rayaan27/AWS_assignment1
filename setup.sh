#!/bin/bash
# ─────────────────────────────────────────────────────────────
# UniEvent — EC2 Setup Script
# Run this on your EC2 instance after connecting via SSH
# Usage: chmod +x setup.sh && sudo ./setup.sh
# ─────────────────────────────────────────────────────────────

echo "======================================"
echo "  UniEvent EC2 Setup Starting..."
echo "======================================"

# 1. Update system
echo "[1/6] Updating system packages..."
apt-get update -y && apt-get upgrade -y

# 2. Install Python and pip
echo "[2/6] Installing Python3 and pip..."
apt-get install -y python3 python3-pip git

# 3. Clone the GitHub repo
echo "[3/6] Cloning GitHub repository..."
cd /home/ubuntu
git clone https://github.com/YOUR_GITHUB_USERNAME/Assignment1_AWS_CE.git
cd Assignment1_AWS_CE

# 4. Install Python libraries
echo "[4/6] Installing Python dependencies..."
pip3 install -r requirements.txt

# 5. Allow port 80
echo "[5/6] Opening port 80..."
ufw allow 80

# 6. Run the Flask app
echo "[6/6] Starting UniEvent app on port 80..."
python3 app.py

echo "======================================"
echo "  App is running! Visit your Load"
echo "  Balancer DNS link in your browser."
echo "======================================"
