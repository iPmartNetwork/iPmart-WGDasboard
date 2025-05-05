#!/bin/bash

set -e

# Clear the screen and display a logo
clear
echo -e "${MAGENTA}"
echo "
____________________________________________________________________________________
        ____                             _     _                                     
    ,   /    )                           /|   /                                  /   
-------/____/---_--_----__---)__--_/_---/-| -/-----__--_/_-----------__---)__---/-__-
  /   /        / /  ) /   ) /   ) /    /  | /    /___) /   | /| /  /   ) /   ) /(    
_/___/________/_/__/_(___(_/_____(_ __/___|/____(___ _(_ __|/_|/__(___/_/_____/___\__
                                                                                     
"
echo "***** https://github.com/ipmartnetwork *****"
echo -e "${RESET}"
echo -e "${CYAN}🌐 Welcome to the iPmart WireGuard Dashboard Installer!${RESET}"

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
RESET='\033[0m'

WG_INTERFACE="wg0"
WG_PORT="51820"
WG_NETWORK="10.0.0.1/24"
WG_CONF_PATH="/etc/wireguard"
DASHBOARD_DIR="/opt/wgdashboard"
DOMAIN=""
EMAIL=""
INTERFACE=""

read -p "$(echo -e "${BLUE}🌐 Enter your dashboard domain (e.g., panel.example.com): ${RESET}")" DOMAIN
read -p "$(echo -e "${BLUE}📧 Enter your email for Let's Encrypt SSL: ${RESET}")" EMAIL

# Detect default network interface
INTERFACE=$(ip route | grep default | awk '{print $5}')
SERVER_IP=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

echo -e "${GREEN}✅ Detected network interface: ${YELLOW}$INTERFACE${RESET}"
echo -e "${GREEN}✅ Server IP: ${YELLOW}$SERVER_IP${RESET}"

echo -e "${CYAN}⏳ Installing WireGuard and required packages...${RESET}"
apt update && apt install -y wireguard qrencode curl nginx python3-pip unzip certbot python3-certbot-nginx python3.10-venv

echo -e "${CYAN}🔐 Generating WireGuard keys...${RESET}"
mkdir -p $WG_CONF_PATH
wg genkey | tee $WG_CONF_PATH/privatekey | wg pubkey > $WG_CONF_PATH/publickey
PRIVATE_KEY=$(cat $WG_CONF_PATH/privatekey)
PUBLIC_KEY=$(cat $WG_CONF_PATH/publickey)

echo -e "${CYAN}📄 Creating WireGuard configuration file...${RESET}"
cat > $WG_CONF_PATH/$WG_INTERFACE.conf <<EOF
[Interface]
PrivateKey = $PRIVATE_KEY
Address = $WG_NETWORK
ListenPort = $WG_PORT
PostUp = iptables -A FORWARD -i $WG_INTERFACE -j ACCEPT; iptables -t nat -A POSTROUTING -o $INTERFACE -j MASQUERADE
PostDown = iptables -D FORWARD -i $WG_INTERFACE -j ACCEPT; iptables -t nat -D POSTROUTING -o $INTERFACE -j MASQUERADE
EOF

echo -e "${CYAN}🔄 Enabling and starting WireGuard...${RESET}"
systemctl enable wg-quick@$WG_INTERFACE
systemctl start wg-quick@$WG_INTERFACE

echo -e "${GREEN}✅ WireGuard setup completed with IP ${YELLOW}$WG_NETWORK${GREEN} and port ${YELLOW}$WG_PORT${RESET}."

echo -e "${CYAN}📦 Downloading iPmart WGDashboard...${RESET}"
mkdir -p $DASHBOARD_DIR
cd /tmp
curl -L -o dashboard.tar.gz "https://github.com/iPmartNetwork/iPmart-WGDasboard/releases/download/1.0.0/wgdashboard.tar.gz"
tar -xzf dashboard.tar.gz -C $DASHBOARD_DIR --strip-components=1

echo -e "${CYAN}📦 Installing Python dependencies for dashboard...${RESET}"
cd $DASHBOARD_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo -e "${CYAN}📦 Verifying Python dependencies...${RESET}"
cd $DASHBOARD_DIR
source venv/bin/activate
if ! pip install -r requirements.txt; then
    echo -e "${RED}❌ Failed to install Python dependencies. Please check the requirements file.${RESET}"
    exit 1
fi

echo -e "${CYAN}🔍 Checking for syntax errors in the application...${RESET}"
if ! python -m py_compile app/__init__.py; then
    echo -e "${RED}❌ Syntax errors detected in the application. Please fix them and try again.${RESET}"
    exit 1
fi

echo -e "${CYAN}🔐 Setting up NGINX and obtaining SSL certificate...${RESET}"
rm -f /etc/nginx/sites-enabled/default
cat > /etc/nginx/sites-available/wgdashboard <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

[ -L /etc/nginx/sites-enabled/wgdashboard ] && rm /etc/nginx/sites-enabled/wgdashboard
ln -s /etc/nginx/sites-available/wgdashboard /etc/nginx/sites-enabled/wgdashboard
nginx -t && systemctl restart nginx

echo -e "${CYAN}⏳ Obtaining SSL certificate with Certbot...${RESET}"
if certbot --nginx -d $DOMAIN --agree-tos --non-interactive --email $EMAIL; then
    echo -e "${GREEN}✅ SSL certificate successfully obtained.${RESET}"
else
    echo -e "${RED}❌ Failed to obtain SSL certificate. Please check Certbot logs.${RESET}"
    exit 1
fi

echo -e "${CYAN}🔁 Reloading NGINX with SSL...${RESET}"
systemctl reload nginx

echo -e "${CYAN}🧰 Setting up dashboard systemd service...${RESET}"
if [ -f $DASHBOARD_DIR/ipmart-dashboard.service ]; then
    cp $DASHBOARD_DIR/ipmart-dashboard.service /etc/systemd/system/
else
    echo -e "${RED}❌ Service file ipmart-dashboard.service not found in $DASHBOARD_DIR.${RESET}"
    exit 1
fi

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable ipmart-dashboard
systemctl start ipmart-dashboard

# Check if the dashboard service is running
if systemctl is-active --quiet ipmart-dashboard; then
    echo -e "${GREEN}✅ Dashboard service is running.${RESET}"
else
    echo -e "${RED}❌ Dashboard service failed to start. Attempting to restart...${RESET}"
    systemctl restart ipmart-dashboard
    sleep 5
    if systemctl is-active --quiet ipmart-dashboard; then
        echo -e "${GREEN}✅ Dashboard service restarted successfully.${RESET}"
    else
        echo -e "${RED}❌ Dashboard service failed to restart. Checking logs...${RESET}"
        journalctl -u ipmart-dashboard | tail -n 20
        exit 1
    fi
fi

echo -e "${CYAN}🔁 Reloading NGINX with SSL...${RESET}"
systemctl reload nginx

# Test NGINX configuration and backend connectivity
echo -e "${CYAN}⏳ Testing NGINX and backend connectivity...${RESET}"
if curl -sI http://127.0.0.1:8000 | grep -q "200 OK"; then
    echo -e "${GREEN}✅ Backend is reachable by NGINX.${RESET}"
else
    echo -e "${RED}❌ Backend is not reachable by NGINX. Checking dashboard service logs...${RESET}"
    journalctl -u ipmart-dashboard | tail -n 20
    exit 1
fi

echo -e "${MAGENTA}🎉 Installation complete! Access your dashboard at: ${YELLOW}https://$DOMAIN${RESET}"
