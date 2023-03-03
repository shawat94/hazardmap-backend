import os
from dotenv import load_dotenv

from api.app import create_app

if __name__ == '__main__':
  load_dotenv()
  env_name = os.getenv('FLASK_ENV')
  app = create_app(env_name)
  app.run()
