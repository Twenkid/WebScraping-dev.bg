import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


FLASK_APP = os.environ.get('FLASK_APP')
FLASK_ENV = os.environ.get('FLASK_ENV')

SERVER = os.environ.get('SQL_SERVER')
DATABASE = os.environ.get('SQL_DATABASE')
UID = os.environ.get('SQL_UID')
PWD = os.environ.get('SQL_PWD')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{UID}:{PWD}@{SERVER}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_POOL_SIZE = 100
