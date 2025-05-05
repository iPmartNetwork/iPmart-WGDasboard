
import os
from flask import Flask
from flask_qrcode import QRcode

def create_app():
    app = Flask(__name__)

    # Use environment variable for SECRET_KEY with a fallback
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize QR code extension
    QRcode(app)

    # Import and register blueprints with error handling
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError as e:
        print(f"Error importing auth blueprint: {e}")

    try:
        from app.routes.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp)
    except ImportError as e:
        print(f"Error importing dashboard blueprint: {e}")

    try:
        from app.routes.config import config_bp
        app.register_blueprint(config_bp)
    except ImportError as e:
        print(f"Error importing config blueprint: {e}")

    try:
        from app.routes.peers import peers_bp
        app.register_blueprint(peers_bp)
    except ImportError as e:
        print(f"Error importing peers blueprint: {e}")

    return app
