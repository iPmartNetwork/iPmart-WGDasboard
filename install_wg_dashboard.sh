# Default values
WG_INTERFACE="wg0"
WG_PORT="51820"
WG_NETWORK="10.0.0.1/24"
WG_CONF_PATH="/etc/wireguard"
DASHBOARD_DIR="/opt/wgdashboard"
DASHBOARD_PORT="8000"  # Default port for the web panel
DOMAIN=""
EMAIL=""
INTERFACE=""

# Prompt user for domain, email, and optionally the dashboard port
read -p "$(echo -e "${BLUE}🌐 Enter your dashboard domain (e.g., panel.example.com): ${RESET}")" DOMAIN
read -p "$(echo -e "${BLUE}📧 Enter your email for Let's Encrypt SSL: ${RESET}")" EMAIL
read -p "$(echo -e "${BLUE}🚪 Enter the port for the dashboard (default: 8000): ${RESET}")" DASHBOARD_PORT_INPUT

# Use the provided port or fallback to the default
DASHBOARD_PORT=${DASHBOARD_PORT_INPUT:-$DASHBOARD_PORT}

# Detect default network interface
INTERFACE=$(ip route | grep default | awk '{print $5}')
SERVER_IP=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

if [[ -z "$INTERFACE" || -z "$SERVER_IP" ]]; then
    echo -e "${RED}❌ Failed to detect network interface or server IP. Please check your network configuration.${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ Detected network interface: ${YELLOW}$INTERFACE${RESET}"
echo -e "${GREEN}✅ Server IP: ${YELLOW}$SERVER_IP${RESET}"
echo -e "${GREEN}✅ Dashboard will run on port: ${YELLOW}$DASHBOARD_PORT${RESET}"

# Install dependencies
echo -e "${CYAN}⏳ Installing WireGuard and required packages...${RESET}"
apt update && apt install -y wireguard qrencode curl nginx python3-pip unzip certbot python3-certbot-nginx python3.10-venv || {
    echo -e "${RED}❌ Failed to install required packages. Please check your package manager.${RESET}"
    exit 1
}

# Set up NGINX
echo -e "${CYAN}🔐 Setting up NGINX and obtaining SSL certificate...${RESET}"
rm -f /etc/nginx/sites-enabled/default
cat > /etc/nginx/sites-available/wgdashboard <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:$DASHBOARD_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/wgdashboard /etc/nginx/sites-enabled/wgdashboard
nginx -t && systemctl restart nginx || {
    echo -e "${RED}❌ Failed to configure NGINX. Please check the configuration.${RESET}"
    exit 1
}

# Set up the dashboard service
echo -e "${CYAN}🧰 Setting up dashboard systemd service...${RESET}"
if [ -f $DASHBOARD_DIR/ipmart-dashboard.service ]; then
    cp $DASHBOARD_DIR/ipmart-dashboard.service /etc/systemd/system/
    sed -i "s/8000/$DASHBOARD_PORT/g" /etc/systemd/system/ipmart-dashboard.service
else
    echo -e "${RED}❌ Service file ipmart-dashboard.service not found in $DASHBOARD_DIR.${RESET}"
    exit 1
fi

systemctl daemon-reload
systemctl enable ipmart-dashboard
systemctl start ipmart-dashboard || {
    echo -e "${RED}❌ Failed to start the dashboard service. Please check the logs.${RESET}"
    exit 1
}

echo -e "${MAGENTA}🎉 Installation complete! Access your dashboard at: ${YELLOW}http://$DOMAIN:$DASHBOARD_PORT${RESET}"
