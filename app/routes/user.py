
import os
import json
from flask import Blueprint, render_template, request, redirect, session, send_file, flash, url_for
from werkzeug.utils import secure_filename

user_bp = Blueprint('user', __name__, url_prefix='/user')

USER_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'user_db.json')

def load_users():
    with open(USER_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user'] = user
                return redirect(url_for('user.dashboard'))
        flash("نام کاربری یا رمز عبور نادرست است", "danger")
    return render_template('user_login.html')

@user_bp.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('user.login'))
    try:
        with open(user['config_path'], 'r') as f:
            config = f.read()
    except:
        config = "فایل کانفیگ یافت نشد."
    return render_template('user_dashboard.html', user=user, config=config)

@user_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('user.login'))

@user_bp.route('/download')
def download():
    user = session.get('user')
    if not user:
        return redirect(url_for('user.login'))
    return send_file(user['config_path'], as_attachment=True)
