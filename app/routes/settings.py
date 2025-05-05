
from flask import Blueprint, request, jsonify
import configparser
import os

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")
CONFIG_PATH = "./config.ini"

def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config

def save_config(config):
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

@settings_bp.route("/update_peer_default_config", methods=["POST"])
def update_peer_default_config():
    data = request.get_json()
    config = get_config()
    config.set("General", "peer_default_config", data.get("value"))
    save_config(config)
    return jsonify({"status": True})

@settings_bp.route("/update_wg_conf_path", methods=["POST"])
def update_wg_conf_path():
    data = request.get_json()
    config = get_config()
    config.set("General", "wg_conf_path", data.get("value"))
    save_config(config)
    return jsonify({"status": True})

@settings_bp.route("/update_acct", methods=["POST"])
def update_acct():
    data = request.get_json()
    config = get_config()
    config.set("Account", "username", data.get("value"))
    save_config(config)
    return jsonify({"status": True})

@settings_bp.route("/update_pwd", methods=["POST"])
def update_pwd():
    import hashlib
    data = request.get_json()
    new_hashed = hashlib.sha256(data.get("value").encode()).hexdigest()
    config = get_config()
    config.set("Account", "password", new_hashed)
    save_config(config)
    return jsonify({"status": True})

@settings_bp.route("/update_app_ip_port", methods=["POST"])
def update_app_ip_port():
    data = request.get_json()
    config = get_config()
    config.set("General", "app_ip", data.get("ip"))
    config.set("General", "app_port", data.get("port"))
    save_config(config)
    return jsonify({"status": True})
