
from flask import Blueprint, render_template, abort, request
from app.core.wgmanager import WireGuardManager
from app.core.system_monitor import SystemMonitor

configuration_bp = Blueprint("configuration", __name__, url_prefix="/configuration")

WG_CONF_PATH = "/etc/wireguard"

@configuration_bp.route("/<conf_name>")
def view_conf(conf_name):
    wg = WireGuardManager(WG_CONF_PATH)
    config_data = wg.get_full_config(conf_name)
    if not config_data:
        return abort(404, "Config not found")

    # شبیه‌سازی داده‌های نمایشی برای template ها
    peer_data = []
    for p in config_data.get("Peers", []):
        peer_data.append({
            "id": p.get("PublicKey", "")[:10],
            "name": "",
            "status": "online" if wg.is_peer_running(conf_name, p.get("PublicKey", "")) else "offline",
            "allowed_ip": p.get("AllowedIPs", ""),
            "latest_handshake": "unknown",
            "endpoint": p.get("Endpoint", ""),
            "total_sent": "0.0",
            "total_receive": "0.0",
            "private_key": p.get("PrivateKey", None)
        })

    conf_info = {
        "name": conf_name,
        "status": wg.get_conf_status(conf_name),
        "public_key": wg.get_conf_pub_key(conf_name),
        "listen_port": wg.get_conf_listen_port(conf_name),
        "conf_address": wg.get_interface_address(conf_name) or "N/A",
        "running_peer": sum(1 for p in peer_data if p["status"] == "online"),
        "total_data_usage": ["0.0", "0.0", "0.0"],
        "checked": "checked" if wg.get_conf_status(conf_name) == "running" else "",
        "peer_data": peer_data
    }

    return render_template("get_conf.html", conf_data=conf_info, sort_tag="status", dashboard_refresh_interval=5000, peer_display_mode="grid")
