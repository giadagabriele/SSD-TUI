import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
env_path = Path('.').resolve().joinpath('.env')
load_dotenv(dotenv_path=env_path)
 
settings = {
  "DEBUG": os.getenv('DEBUG'),
  "SECRET_KEY": os.getenv('SECRET_KEY'),
  "BASE_URL": os.getenv('BASE_URL'),
  "SUPERUSER_USERNAME": os.getenv('SUPERUSER_USERNAME'),
  "SUPERUSER_PASSWORD": os.getenv('SUPERUSER_PASSWORD'),
  "STAFF_USERNAME": os.getenv('STAFF_USERNAME'),
  "STAFF_PASSWORD": os.getenv('STAFF_PASSWORD'),
  "USER_USERNAME": os.getenv('USER_USERNAME'),
  "USER_PASSWORD": os.getenv('USER_PASSWORD'),
}