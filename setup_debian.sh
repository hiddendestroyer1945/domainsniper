#!/bin/bash

# setup_debian.sh - Installation script for DomainSniper
# Compatible with Debian 12

echo "[*] Initializing DomainSniper Setup..."

# Ensure Tor is installed
if ! command -v tor &> /dev/null; then
    echo "[*] Installing dependencies (Tor, Python tools)..."
    sudo apt update && sudo apt install -y tor python3-pip python3-venv
    sudo systemctl enable tor
    sudo systemctl start tor
else
    echo "[+] Tor is already installed."
fi

# Setup Python Virtual Environment
echo "[*] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Setup complete!"
echo "[*] To run the program: source venv/bin/activate && python3 domainsniper.py"
