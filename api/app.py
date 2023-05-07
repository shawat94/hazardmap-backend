import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import get_config
from .models import db, bcrypt
from .controllers.UserController import user_api as user_blueprint
from .controllers.HazardController import hazard_api as hazard_blueprint


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(get_config[env_name])

    app.register_blueprint(user_blueprint)
    app.register_blueprint(hazard_blueprint)

    CORS(app, resources={r'/*': {'origins': os.getenv('ALLOWED_ORIGINS')}},
         supports_credentials=True
         )
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)

    @app.route('/api/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Test endpoint'

    return app
