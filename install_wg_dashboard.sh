#!/bin/bash

set -e

WG_INTERFACE="wg0"
WG_PORT="51820"
WG_NETWORK="10.0.0.1/24"
WG_CONF_PATH="/etc/wireguard"
DASHBOARD_DIR="/opt/wgdashboard"
DOMAIN=""
EMAIL=""
INTERFACE=""

read -p "🌐 Enter your dashboard domain (e.g., panel.example.com): " DOMAIN
read -p "📧 Enter your email for Let's Encrypt SSL: " EMAIL

# Detect default network interface
INTERFACE=$(ip route | grep default | awk '{print $5}')
SERVER_IP=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

echo "✅ Detected network interface: $INTERFACE"
echo "✅ Server IP: $SERVER_IP"

echo "⏳ Installing WireGuard and required packages..."
apt update && apt install -y wireguard qrencode curl nginx python3-pip unzip certbot python3-certbot-nginx

echo "🔐 Generating WireGuard keys..."
mkdir -p $WG_CONF_PATH
wg genkey | tee $WG_CONF_PATH/privatekey | wg pubkey > $WG_CONF_PATH/publickey
PRIVATE_KEY=$(cat $WG_CONF_PATH/privatekey)
PUBLIC_KEY=$(cat $WG_CONF_PATH/publickey)

echo "📄 Creating WireGuard configuration file..."
cat > $WG_CONF_PATH/$WG_INTERFACE.conf <<EOF
[Interface]
PrivateKey = $PRIVATE_KEY
Address = $WG_NETWORK
ListenPort = $WG_PORT
PostUp = iptables -A FORWARD -i $WG_INTERFACE -j ACCEPT; iptables -t nat -A POSTROUTING -o $INTERFACE -j MASQUERADE
PostDown = iptables -D FORWARD -i $WG_INTERFACE -j ACCEPT; iptables -t nat -D POSTROUTING -o $INTERFACE -j MASQUERADE
EOF

echo "🔄 Enabling and starting WireGuard..."
systemctl enable wg-quick@$WG_INTERFACE
systemctl start wg-quick@$WG_INTERFACE

echo "✅ WireGuard setup completed with IP $WG_NETWORK and port $WG_PORT."

echo "📦 Downloading iPmart WGDashboard..."
mkdir -p $DASHBOARD_DIR
cd /tmp
curl -L -o dashboard.tar.gz "https://github.com/iPmartNetwork/iPmart-WGDasboard/releases/download/1.0.0/wgdashboard.tar.gz"
tar -xzf dashboard.tar.gz -C $DASHBOARD_DIR --strip-components=1

echo "📦 Installing Python dependencies for dashboard..."
cd $DASHBOARD_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "🔐 Setting up NGINX and obtaining SSL certificate..."
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

echo "⏳ Obtaining SSL certificate with Certbot..."
if certbot --nginx -d $DOMAIN --agree-tos --non-interactive --email $EMAIL; then
    echo "✅ SSL certificate successfully obtained."
else
    echo "❌ Failed to obtain SSL certificate. Please check Certbot logs."
    exit 1
fi

echo "🔁 Reloading NGINX with SSL..."
systemctl reload nginx

echo "🧰 Setting up dashboard systemd service..."
if [ -f $DASHBOARD_DIR/ipmart-dashboard.service ]; then
    cp $DASHBOARD_DIR/ipmart-dashboard.service /etc/systemd/system/
else
    echo "❌ Service file ipmart-dashboard.service not found in $DASHBOARD_DIR."
    exit 1
fi

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable ipmart-dashboard
systemctl start ipmart-dashboard

# Check if the dashboard service is running
if systemctl is-active --quiet ipmart-dashboard; then
    echo "✅ Dashboard service is running."
else
    echo "❌ Dashboard service failed to start. Check logs with: journalctl -u ipmart-dashboard"
    exit 1
fi

echo "🔁 Reloading NGINX with SSL..."
systemctl reload nginx

# Test NGINX configuration and backend connectivity
echo "⏳ Testing NGINX and backend connectivity..."
if curl -sI http://127.0.0.1:8000 | grep -q "200 OK"; then
    echo "✅ Backend is reachable by NGINX."
else
    echo "❌ Backend is not reachable by NGINX. Check the dashboard service and firewall settings."
    exit 1
fi

echo "✅ Installation complete! Access your dashboard at: https://$DOMAIN"
