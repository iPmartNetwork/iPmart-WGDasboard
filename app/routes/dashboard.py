from flask import Blueprint, render_template, jsonify, current_app
from app.core.wgmanager import WireGuardManager
import os

dashboard_bp = Blueprint('dashboard', __name__)

# Use environment variable or default path for WireGuard configuration
WG_CONF_PATH = os.getenv("WG_CONF_PATH", "/etc/wireguard")

def get_interface_details(wg):
    """Helper function to fetch interface details."""
    try:
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
        return interface_list
    except Exception as e:
        current_app.logger.error(f"Error fetching interface details: {e}")
        return []

@dashboard_bp.route('/')
def index():
    try:
        wg = WireGuardManager(WG_CONF_PATH)
        interface_list = get_interface_details(wg)
        return render_template('dashboard.html', interfaces=interface_list)
    except Exception as e:
        current_app.logger.error(f"Error rendering dashboard: {e}")
        return render_template('error.html', message="An error occurred while loading the dashboard"), 500

@dashboard_bp.route('/api/interfaces')
def interface_list_json():
    try:
        wg = WireGuardManager(WG_CONF_PATH)
        interface_list = get_interface_details(wg)
        return jsonify(interface_list)
    except Exception as e:
        current_app.logger.error(f"Error fetching interface list as JSON: {e}")
        return jsonify({"error": "An error occurred while fetching interface data"}), 500
