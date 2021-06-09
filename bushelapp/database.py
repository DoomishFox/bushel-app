import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from .aws_secrets_manager import get_secret

awsrds_block = json.load(get_secret("rds_connstr", "dev"))
awsrds_connstr = awsrds_block['engine'] + '+pymysql://' + awsrds_block['username'] + ':' + awsrds_block['password'] + '@' + awsrds_block['host'] + ':' + awsrds_block['port'] + '/' + awsrds_block['dbname']
engine = create_engine(awsrds_connstr, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

awsdocdb_block = json.load(get_secret("docdb_connstr", "dev"))
awsdocdb_connstr = awsdocdb_block['engine'] + '://' + awsdocdb_block['username'] + ':' + awsdocdb_block['password'] + '@' + awsdocdb_block['host'] + ':' + awsdocdb_block['port'] + '/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
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