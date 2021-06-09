import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient

awsrds_connstr = os.environ['RDS_CONNSTR']
engine = create_engine(awsrds_connstr, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

awsdocdb_connstr = os.environ['DOCDB_CONNSTR']
docdb_client = MongoClient(awsdocdb_connstr)
docdb_session = docdb_client.bushelcontent

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from .models import User, AuthToken, Leaf, Branch, Root
    Base.metadata.create_all(bind=engine)

def destroy_db():
    # destroy all scheme and content in the database
    Base.metadata.drop_all(bind=engine)
    docdb_session.leafmd.delete_many({})
    docdb_session.leafhtml.delete_many({})

def shutdown_session(exception=None):
    db_session.remove()
    docdb_client.close()