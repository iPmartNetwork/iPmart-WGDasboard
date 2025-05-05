from flask import Blueprint, render_template, abort, current_app
from app.core.wgmanager import WireGuardManager
import os

config_bp = Blueprint('config', __name__, url_prefix="/config")

# Use environment variable or default path for WireGuard configuration
WG_CONF_PATH = os.getenv("WG_CONF_PATH", "/etc/wireguard")

@config_bp.route('/<config_name>')
def config_detail(config_name):
    try:
        # Validate config_name to prevent directory traversal attacks
        if not config_name.isalnum():
            abort(400, "Invalid configuration name")

        wg = WireGuardManager(WG_CONF_PATH)
        config = wg.get_full_config(config_name)

        if not config:
            abort(404, "Configuration not found")

        return render_template('config_detail.html', config=config, config_name=config_name)
    except Exception as e:
        # Log the error for debugging
        current_app.logger.error(f"Error retrieving configuration '{config_name}': {e}")
        abort(500, "An internal error occurred while retrieving the configuration")
