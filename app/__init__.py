
from flask import Flask
from flask_qrcode import QRcode

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "your-secret-key"
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    QRcode(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.config import config_bp
    from app.routes.peers import peers_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(peers_bp)

    return app
