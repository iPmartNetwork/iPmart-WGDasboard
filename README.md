![iPmart WGDashboard](static/logo.svg)


# iPmart WGDashboard

یک داشبورد کامل و مدرن برای مدیریت WireGuard، طراحی‌شده برای محیط‌های فارسی با امکانات قدرتمند مدیریتی و API.

---

## 🚀 ویژگی‌ها

- 🎨 رابط کاربری فارسی و راست‌چین (RTL)
- 📦 بکاپ‌گیری و بازیابی کانفیگ
- 🤖 ارسال پیام و فایل بکاپ به ربات تلگرام
- 👤 پنل کاربری اختصاصی با QR Code و دانلود فایل
- 📈 گراف زنده مصرف CPU, RAM, TX/RX
- 🧩 API REST با احراز هویت توکنی
- 🛠️ نصب آسان با systemd و اسکریپت آماده

---

## ⚙️ نصب سریع

```bash
git clone https://github.com/iPmartNetwork/iPmart-WGDasboard.git
cd iPmart-WGDasboard
apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🖥️ اجرا

```bash
python run.py
```

یا با systemd:

```bash
sudo cp ipmart-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl start ipmart-dashboard
sudo systemctl enable ipmart-dashboard
```

---

## 🔐 فایل `.env` نمونه

```
API_TOKEN=your_api_token
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 📡 API REST

| مسیر | متد | توضیح |
|------|-----|--------|
| `/api/peers` | GET | لیست کاربران |
| `/api/peer/add` | POST | افزودن کاربر |
| `/api/peer/delete` | POST | حذف کاربر |

هدر لازم:
```
Authorization: Bearer your_api_token
```

---

## 👤 دسترسی کاربر

- مسیر ورود: `/user/login`
- نمایش کانفیگ، QR و دانلود فایل

---

## 📈 گراف منابع

- آدرس JSON: `/system/stats`
- بروزرسانی لحظه‌ای در داشبورد

---

## 🔗 مجوز
MIT
