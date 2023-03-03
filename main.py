from flask_restful import Api
from resources import Hazards, \
    Areas, Users
from models import db
from flask_migrate import Migrate
from api.app import create_app


app = create_app()
migrate = Migrate(app, db)


# API
api = Api(app)
api.add_resource(Hazards, '/healthcheck')
api.add_resource(Areas, '/api/users')
api.add_resource(Users, '/api/user/<username>')