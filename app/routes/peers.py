
from flask import Blueprint, request, jsonify, abort
from app.core.wgmanager import WireGuardManager

peers_bp = Blueprint('peers', __name__, url_prefix="/peers")

WG_CONF_PATH = "/etc/wireguard"

@peers_bp.route('/<config_name>', methods=["GET"])
def list_peers(config_name):
    wg = WireGuardManager(WG_CONF_PATH)
    config = wg.get_full_config(config_name)
    if not config:
        return abort(404, "Config not found")
    return jsonify(config.get("Peers", []))

@peers_bp.route('/<config_name>/add', methods=["POST"])
def add_peer(config_name):
    data = request.get_json()
    # این بخش را می‌توان با اعتبارسنجی قوی‌تر کامل‌تر کرد
    peer_config = f"""
[Peer]
PublicKey = {data.get("PublicKey")}
AllowedIPs = {data.get("AllowedIPs")}
"""
    conf_path = f"{WG_CONF_PATH}/{config_name}.conf"
    try:
        with open(conf_path, "a") as conf_file:
            conf_file.write(peer_config)
        return jsonify({"status": True, "msg": "Peer added."})
    except Exception as e:
        return jsonify({"status": False, "msg": str(e)})

@peers_bp.route('/<config_name>/remove', methods=["POST"])
def remove_peer(config_name):
    data = request.get_json()
    pubkey_to_remove = data.get("PublicKey")
    wg = WireGuardManager(WG_CONF_PATH)
    config = wg.get_full_config(config_name)

    if not config:
        return abort(404, "Config not found")

    new_peers = [peer for peer in config["Peers"] if peer.get("PublicKey") != pubkey_to_remove]
    if len(new_peers) == len(config["Peers"]):
        return jsonify({"status": False, "msg": "Peer not found"})

    # بازنویسی کامل فایل کانفیگ
    try:
        with open(f"{WG_CONF_PATH}/{config_name}.conf", "w") as f:
            f.write("[Interface]\n")
            for key, val in config["Interface"].items():
                f.write(f"{key} = {val}\n")
            for peer in new_peers:
                f.write("\n[Peer]\n")
                for key, val in peer.items():
                    f.write(f"{key} = {val}\n")
        return jsonify({"status": True, "msg": "Peer removed"})
    except Exception as e:
        return jsonify({"status": False, "msg": str(e)})
