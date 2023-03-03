from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import get_config
from .models import db, bcrypt
from.controllers.UserController import user_api as user_blueprint

db = SQLAlchemy()


def create_app(env_name):

    app = Flask(__name__)
    app.config.from_object(get_config[env_name])

    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Test endpoint'

    return app