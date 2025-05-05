
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

## ⚙️ Installation

```bash
git clone https://github.com/yourname/ipmart-wgdashboard.git
cd ipmart-wgdashboard
pip install -r requirements.txt
python run.py
```

> Default runs on: `http://localhost:8000`

---

## ⚠️ Configuration

Edit `config.ini` to set username, password (SHA256 hash), panel port, WireGuard path, and Telegram bot token/chat ID.

---

## 🧪 Development

- Python 3.9+
- Flask
- Bootstrap 5 (RTL)
- jQuery, Chart.js
- Telegram Bot API

---

## 🌍 ترجمه فارسی

### 🎯 امکانات داشبورد iPmart

- مدیریت کامل اینترفیس‌ها و کاربران WireGuard
- مانیتور زنده مصرف RAM و CPU
- پینگ و ترک‌روت مستقیم از پنل
- دانلود فایل کانفیگ و QR برای اتصال سریع
- لاگین امن با نام کاربری و رمز هش‌شده
- بکاپ‌گیری، بازگردانی و حذف
- ارسال هشدار و فایل به تلگرام
- طراحی حرفه‌ای با بوت‌استرپ راست‌چین

---

### ⚙️ نصب سریع

```bash
git clone https://github.com/yourname/ipmart-wgdashboard.git
cd ipmart-wgdashboard
pip install -r requirements.txt
python run.py
```

- آدرس پیش‌فرض: `http://localhost:8000`
- اطلاعات ورود: در `config.ini`

---

### ☎️ ارتباط با ما

برای پشتیبانی یا پیشنهاد ویژگی جدید لطفاً Issue باز کنید یا از طریق تلگرام تماس بگیرید.

---

🔐 تحت مجوز MIT منتشر شده است.
