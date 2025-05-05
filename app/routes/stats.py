
import psutil
from flask import Blueprint, jsonify

stats_bp = Blueprint('stats', __name__, url_prefix='/system')

@stats_bp.route('/stats')
def get_system_stats():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    net = psutil.net_io_counters()
    stats = {
        "cpu": cpu,
        "ram": ram,
        "tx": round(net.bytes_sent / 1024 / 1024, 2),   # MB
        "rx": round(net.bytes_recv / 1024 / 1024, 2)    # MB
    }
    return jsonify(stats)
