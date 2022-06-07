__version__ = '0.0.3'

from datetime import timedelta

from flask import Flask, session, jsonify
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
# from flask_mail import Mail
import os
import flask_monitoringdashboard as dashboard
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
migrate = Migrate()
sock = SocketIO(cors_allowed_origins='*')
# mail = Mail()

def create_app():
    app = Flask(__name__, 
            static_url_path='/files', 
            static_folder='product_imgs',
            template_folder='templates')
    
    app.config.from_prefixed_env()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365*2)
    app.config['SESSION_COOKIE_DOMAIN'] = "stolovaya.online"
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['JSON_AS_ASCII'] = False
    app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
    app.secret_key = os.environ.get("APP_SECRET")
    app.url_map.strict_slashes = False

    

    jwt = JWTManager(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    migrate.init_app(app, db)
    # mail.init_app(app)
    dashboard.bind(app)


    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .api.api import kitchen_api
    app.register_blueprint(kitchen_api)

    
    sock.init_app(app, cors_allowed_origins="*")
    return app

