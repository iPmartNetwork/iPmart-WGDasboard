import os
import json
from datetime import datetime

# Ensure apscheduler is installed
try:
    import apscheduler
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'apscheduler'])

from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.telegram_alert import send_telegram_message, send_telegram_file

BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', 'backups')

def auto_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    config = {
        "interface": {
            "Address": "10.0.0.1/24",
            "ListenPort": 51820,
            "PrivateKey": "PRIVATE_KEY"
        },
        "peers": [
            {"name": "client1", "ip": "10.0.0.2", "public_key": "PUBKEY1"},
            {"name": "client2", "ip": "10.0.0.3", "public_key": "PUBKEY2"}
        ]
    }

    filename = f"autobackup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(BACKUP_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    send_telegram_message("🕒 بکاپ خودکار انجام شد.")
    send_telegram_file(filepath, "📦 بکاپ خودکار WireGuard")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_backup, 'interval', hours=12)
    scheduler.start()
