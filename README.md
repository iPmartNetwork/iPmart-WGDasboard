
# iPmart WGDashboard

🌐 A modern web dashboard for managing WireGuard VPN servers with real-time monitoring, peer management, configuration tools, and Telegram integration.

---

## 🚀 Features

- ✅ Manage WireGuard interfaces and peers (add/remove/edit)
- 📊 Live monitoring (CPU, RAM, Network)
- 🧰 Tools: Ping / Traceroute
- 🧾 QR code & config download for each peer
- 🔐 Secure login (config-based)
- 🔄 Automatic backup, restore & delete
- 📤 Telegram alerts with backup sending
- 🧩 Bootstrap RTL UI with dark mode
- 📦 Fully modular Flask + Jinja2 backend

---

## ⚙️ Easy Automated Installation (Recommended)

Use the provided Bash installer to set up everything in minutes, including:
- WireGuard installation
- Server key generation
- NAT and routing setup
- WGDashboard deployment (Python/Flask)
- SSL via Let's Encrypt
- systemd service for persistent dashboard startup

### 📥 How to Run

```bash
bash <(curl -Ls https://raw.githubusercontent.com/iPmartNetwork/iPmart-WGDasboard/master/install_wg_dashboard.sh

```

> You’ll be prompted for:
> - Your dashboard domain (e.g. panel.example.com)
> - An email address for SSL certification

---

## 🧪 Manual Development Setup (Alternative)

```bash
git clone https://github.com/yourname/ipmart-wgdashboard.git
cd ipmart-wgdashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

---

## 🌍 فارسی - نصب خودکار

```bash
bash <(curl -Ls https://raw.githubusercontent.com/iPmartNetwork/iPmart-WGDasboard/master/install_wg_dashboard.sh

```

> اطلاعات لازم: دامنه برای SSL و ایمیل شما

✅ همه‌چیز از صفر تا صد: WireGuard + داشبورد + SSL

---

## 🔐 Config

- Edit `config.ini` to change:
  - username/password
  - default peer config
  - WireGuard config path
  - Telegram bot token and chat_id

---

## 📜 License

MIT License
