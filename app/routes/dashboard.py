
from flask import Blueprint, render_template, jsonify
from app.core.wgmanager import WireGuardManager

dashboard_bp = Blueprint('dashboard', __name__)

# مسیر کانفیگ‌های WireGuard
WG_CONF_PATH = "/etc/wireguard"

@dashboard_bp.route('/')
def index():
    wg = WireGuardManager(WG_CONF_PATH)
    interfaces = wg.get_config_names()
    interface_list = []
    for iface in interfaces:
        interface_list.append({
            'name': iface,
            'status': wg.get_conf_status(iface),
            'pubkey': wg.get_conf_pub_key(iface),
            'listen_port': wg.get_conf_listen_port(iface),
            'address': wg.get_interface_address(iface),
        })
    return render_template('dashboard.html', interfaces=interface_list)

@dashboard_bp.route('/api/interfaces')
def interface_list_json():
    wg = WireGuardManager(WG_CONF_PATH)
    interfaces = wg.get_config_names()
    results = []
    for iface in interfaces:
        results.append({
            'name': iface,
            'status': wg.get_conf_status(iface),
            'pubkey': wg.get_conf_pub_key(iface),
            'listen_port': wg.get_conf_listen_port(iface),
            'address': wg.get_interface_address(iface),
        })
    return jsonify(results)
