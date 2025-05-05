
import os
import json
from app.utils.telegram_alert import send_telegram_message, send_telegram_file
from flask import Blueprint, send_file, flash, redirect, request, render_template
from datetime import datetime

backup_bp = Blueprint('backup', __name__)
BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', 'backups')

@backup_bp.route('/backup')
def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Fake config and peers data for now (replace with real sources)
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

    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(BACKUP_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    return send_file(filepath, as_attachment=True)

@backup_bp.route('/restore', methods=['GET', 'POST'])
def restore_backup():
    if request.method == 'POST':
        file = request.files.get('backup_file')
        if file and file.filename.endswith('.json'):
            data = json.load(file)
            # TODO: apply restored data (interface + peers)
            flash("بکاپ با موفقیت بازیابی شد", "success")
            return redirect('/')
        else:
            flash("فایل نامعتبر است", "danger")
    
    return render_template('restore_backup.html')
