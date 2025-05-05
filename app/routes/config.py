
from flask import Blueprint, render_template, abort
from app.core.wgmanager import WireGuardManager

config_bp = Blueprint('config', __name__, url_prefix="/config")

WG_CONF_PATH = "/etc/wireguard"

@config_bp.route('/<config_name>')
def config_detail(config_name):
    wg = WireGuardManager(WG_CONF_PATH)
    config = wg.get_full_config(config_name)
    if not config:
        return abort(404, "Config not found")
    return render_template('config_detail.html', config=config, config_name=config_name)
