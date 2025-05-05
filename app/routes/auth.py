
from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
import hashlib
import configparser

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
CONFIG_PATH = "./config.ini"

def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config

@auth_bp.route("/signin", methods=["GET"])
def signin():
    return render_template("signin.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    config = get_config()
    saved_user = config.get("Account", "username")
    saved_hash = config.get("Account", "password")

    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    if username == saved_user and hashed_input == saved_hash:
        session["username"] = username
        return jsonify({"status": True})
    return jsonify({"status": False, "msg": "نام کاربری یا رمز عبور نادرست است."})

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.signin"))

@auth_bp.route("/status")
def status():
    return jsonify({"authenticated": "username" in session})
