import os
from dotenv import load_dotenv

from api.app import create_app

load_dotenv()
env_name = os.getenv('FLASK_ENV')
hazardmap_app = create_app(env_name)
