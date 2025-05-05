from flask import Blueprint, request, jsonify, abort, current_app
from app.core.wgmanager import WireGuardManager
import os

peers_bp = Blueprint('peers', __name__, url_prefix="/peers")

# Use environment variable or default path for WireGuard configuration
WG_CONF_PATH = os.getenv("WG_CONF_PATH", "/etc/wireguard")

@peers_bp.route('/<config_name>', methods=["GET"])
def list_peers(config_name):
    try:
        wg = WireGuardManager(WG_CONF_PATH)
        config = wg.get_full_config(config_name)
        if not config:
            abort(404, "Config not found")
        return jsonify(config.get("Peers", []))
    except Exception as e:
        current_app.logger.error(f"Error listing peers for {config_name}: {e}")
        return jsonify({"status": False, "msg": "An error occurred while listing peers"}), 500

@peers_bp.route('/<config_name>/add', methods=["POST"])
def add_peer(config_name):
    try:
        data = request.get_json()
        public_key = data.get("PublicKey")
        allowed_ips = data.get("AllowedIPs")

        # Validate input
        if not public_key or not allowed_ips:
            return jsonify({"status": False, "msg": "PublicKey and AllowedIPs are required"}), 400

        peer_config = f"""
[Peer]
PublicKey = {public_key}
AllowedIPs = {allowed_ips}
"""
        conf_path = f"{WG_CONF_PATH}/{config_name}.conf"

        # Append the new peer to the configuration file
        with open(conf_path, "a") as conf_file:
            conf_file.write(peer_config)

        return jsonify({"status": True, "msg": "Peer added."})
    except Exception as e:
        current_app.logger.error(f"Error adding peer to {config_name}: {e}")
        return jsonify({"status": False, "msg": "An error occurred while adding the peer"}), 500

@peers_bp.route('/<config_name>/remove', methods=["POST"])
def remove_peer(config_name):
    try:
        data = request.get_json()
        pubkey_to_remove = data.get("PublicKey")

        # Validate input
        if not pubkey_to_remove:
            return jsonify({"status": False, "msg": "PublicKey is required"}), 400

        wg = WireGuardManager(WG_CONF_PATH)
        config = wg.get_full_config(config_name)

        if not config:
            abort(404, "Config not found")

        # Filter out the peer to be removed
        new_peers = [peer for peer in config["Peers"] if peer.get("PublicKey") != pubkey_to_remove]
        if len(new_peers) == len(config["Peers"]):
            return jsonify({"status": False, "msg": "Peer not found"})

        # Rewrite the configuration file
        conf_path = f"{WG_CONF_PATH}/{config_name}.conf"
        with open(conf_path, "w") as conf_file:
            conf_file.write("[Interface]\n")
            for key, val in config["Interface"].items():
                conf_file.write(f"{key} = {val}\n")
            for peer in new_peers:
                conf_file.write("\n[Peer]\n")
                for key, val in peer.items():
                    conf_file.write(f"{key} = {val}\n")

        return jsonify({"status": True, "msg": "Peer removed"})
    except Exception as e:
        current_app.logger.error(f"Error removing peer from {config_name}: {e}")
        return jsonify({"status": False, "msg": "An error occurred while removing the peer"}), 500
