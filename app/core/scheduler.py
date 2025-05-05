import os
import json
from datetime import datetime

from app.utils.telegram_alert import send_telegram_message, send_telegram_file

BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', 'backups')
