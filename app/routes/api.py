
import json
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from functools import wraps
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

from app.core.system_monitor import get_peer_statuses

API_TOKEN = os.getenv("API_TOKEN", "changeme123")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@api_bp.route('/peers', methods=['GET'])
@swag_from({
    'tags': ['Peers'],
    'summary': 'لیست کاربران',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'لیست کاربران',
            'examples': {'application/json': [{"name": "client1", "ip": "10.0.0.2"}]}
        }
    }
})
@token_required
def get_peers():
    # Dummy data, replace with real data
    peer_statuses = get_peer_statuses()
    from app.core.system_monitor import check_limits
    import json
    with open('app/user_db.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    peer_statuses = check_limits(peer_statuses, users)
    peers = [
        {"name": "client1", "ip": "10.0.0.2", "status": "active", "connected": True},
        {"name": "client2", "ip": "10.0.0.3", "status": "inactive"}
    ]
    return jsonify(peers)

@api_bp.route('/peer/add', methods=['POST'])
@swag_from({
    'tags': ['Peers'],
    'summary': 'افزودن کاربر جدید',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'schema': {
            'type': 'object',
            'properties': {'name': {'type': 'string'}}
        }
    }],
    'responses': {201: {'description': 'کاربر اضافه شد'}}
})
@token_required
def add_peer():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request"}), 400
    # TODO: Add peer logic here
    return jsonify({"message": f"Peer {data['name']} added"}), 201

@api_bp.route('/peer/delete', methods=['POST'])
@swag_from({
    'tags': ['Peers'],
    'summary': 'حذف کاربر',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'schema': {
            'type': 'object',
            'properties': {'name': {'type': 'string'}}
        }
    }],
    'responses': {200: {'description': 'کاربر حذف شد'}}
})
@token_required
def delete_peer():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request"}), 400
    # TODO: Delete peer logic here
    return jsonify({"message": f"Peer {data['name']} deleted"}), 200
