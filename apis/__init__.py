from flask_restplus import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_POOL_SIZE

# Todor debug code: print should be a log, but that's fine for a test
# Create the DB connection
print("Attempt to create a DB engine...")
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=SQLALCHEMY_POOL_SIZE)
print("Success..." + SQLALCHEMY_DATABASE_URI + ": " + str(SQLALCHEMY_POOL_SIZE))
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=engine))
print("AFT session = scoped_session(...")
Base = declarative_base()
Base.query = session.query_property()
print("AFT Base.query")
from . import models
Base.metadata.create_all(bind=engine)
print("AFT Base.metadata.create_all(bind=engine)")
print("After Base.metadata.create_all(bind=engine)...")
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
