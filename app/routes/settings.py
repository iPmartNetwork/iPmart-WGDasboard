from flask import Blueprint, request, jsonify
import configparser
import os
import bcrypt

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")
CONFIG_PATH = os.getenv("CONFIG_PATH", "./config.ini")

def get_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
    config.read(CONFIG_PATH)
    return config

def save_config(config):
    try:
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        raise IOError(f"Error saving configuration: {e}")

@settings_bp.route("/update_peer_default_config", methods=["POST"])
def update_peer_default_config():
    try:
        data = request.get_json()
        value = data.get("value")
        if not value:
            return jsonify({"status": False, "msg": "Value is required"}), 400

        config = get_config()
        config.set("General", "peer_default_config", value)
        save_config(config)
        return jsonify({"status": True})
    except Exception as e:
        return jsonify({"status": False, "msg": f"An error occurred: {e}"}), 500

@settings_bp.route("/update_wg_conf_path", methods=["POST"])
def update_wg_conf_path():
    try:
        data = request.get_json()
        value = data.get("value")
        if not value:
            return jsonify({"status": False, "msg": "Value is required"}), 400

        config = get_config()
        config.set("General", "wg_conf_path", value)
        save_config(config)
        return jsonify({"status": True})
    except Exception as e:
        return jsonify({"status": False, "msg": f"An error occurred: {e}"}), 500

@settings_bp.route("/update_acct", methods=["POST"])
def update_acct():
    try:
        data = request.get_json()
        username = data.get("value")
        if not username:
            return jsonify({"status": False, "msg": "Username is required"}), 400

        config = get_config()
        config.set("Account", "username", username)
        save_config(config)
        return jsonify({"status": True})
    except Exception as e:
        return jsonify({"status": False, "msg": f"An error occurred: {e}"}), 500

@settings_bp.route("/update_pwd", methods=["POST"])
def update_pwd():
    try:
        data = request.get_json()
        password = data.get("value")
        if not password:
            return jsonify({"status": False, "msg": "Password is required"}), 400

        # Use bcrypt for secure password hashing
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        config = get_config()
        config.set("Account", "password", hashed_password)
        save_config(config)
        return jsonify({"status": True})
    except Exception as e:
        return jsonify({"status": False, "msg": f"An error occurred: {e}"}), 500

@settings_bp.route("/update_app_ip_port", methods=["POST"])
def update_app_ip_port():
    try:
        data = request.get_json()
        ip = data.get("ip")
        port = data.get("port")
        if not ip or not port:
            return jsonify({"status": False, "msg": "IP and Port are required"}), 400

        config = get_config()
        config.set("General", "app_ip", ip)
        config.set("General", "app_port", port)
        save_config(config)
        return jsonify({"status": True})
    except Exception as e:
        return jsonify({"status": False, "msg": f"An error occurred: {e}"}), 500
