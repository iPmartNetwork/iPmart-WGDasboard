from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
import bcrypt
import configparser
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
CONFIG_PATH = "./config.ini"

def get_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
    config.read(CONFIG_PATH)
    return config

@auth_bp.route("/signin", methods=["GET"])
def signin():
    return render_template("signin.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"status": False, "msg": "نام کاربری و رمز عبور الزامی است."}), 400

        config = get_config()
        saved_user = config.get("Account", "username", fallback=None)
        saved_hash = config.get("Account", "password", fallback=None)

        if not saved_user or not saved_hash:
            return jsonify({"status": False, "msg": "پیکربندی حساب کاربری ناقص است."}), 500

        if username == saved_user and bcrypt.checkpw(password.encode(), saved_hash.encode()):
            session["username"] = username
            session.permanent = True  # Make the session permanent (can be configured)
            return jsonify({"status": True})
        return jsonify({"status": False, "msg": "نام کاربری یا رمز عبور نادرست است."}), 401
    except Exception as e:
        return jsonify({"status": False, "msg": f"خطا در ورود: {str(e)}"}), 500

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.signin"))

@auth_bp.route("/status")
def status():
    return jsonify({"authenticated": "username" in session})
