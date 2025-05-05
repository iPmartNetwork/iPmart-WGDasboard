
import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token یا Chat ID تنظیم نشده است.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print("Telegram Error:", e)
        return False

def send_telegram_file(filepath, caption=""):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token یا Chat ID تنظیم نشده است.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(filepath, 'rb') as file:
            response = requests.post(url, data={
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption
            }, files={"document": file})
        return response.status_code == 200
    except Exception as e:
        print("Telegram File Error:", e)
        return False
