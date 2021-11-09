from flask_restplus import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_POOL_SIZE

# Create the DB connection
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=SQLALCHEMY_POOL_SIZE)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from . import models
Base.metadata.create_all(bind=engine)

# Create the API
api = Api(
    title='Web Scraping',
    version='1.0',
    description='A short API for Web Scraping',
    # All API metadatas
)

# Add the individual namespaces to the API
from .examples_api import api as examples_namespace
from .dev_bg_api import api as dev_bg_namespace

api.add_namespace(examples_namespace)
api.add_namespace(dev_bg_namespace)
