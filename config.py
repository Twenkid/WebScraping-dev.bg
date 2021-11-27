import os

from dotenv import load_dotenv

print("Config?===================")
#cmd /v /c "set SQL_SERVER=localhost&&set SQL_UID=root&& set SQL_PWD=flask123&&set SQL_DATABASE=flask&&python app.py"

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


FLASK_APP = os.environ.get('FLASK_APP')
FLASK_ENV = os.environ.get('FLASK_ENV')

SERVER = os.environ.get('SQL_SERVER')
DATABASE = os.environ.get('SQL_DATABASE')
UID = os.environ.get('SQL_UID')
PWD = os.environ.get('SQL_PWD')

print("PWD=?",PWD)

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{UID}:{PWD}@{SERVER}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_POOL_SIZE = 100

print("============ END Config?===================")