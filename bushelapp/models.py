import time
import uuid
from sqlalchemy import Column, String, Boolean, Text, Integer, Float, Time, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    alias = Column(String(100))
    password = Column(String(100), nullable=False)

    def __init__(self, username=None, alias=None):
        self.username = username
        self.alias = alias
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(128), unique=True, nullable=False)
    user_id = Column(Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False,)
    issued = Column(Float, nullable=False,
        default=lambda: int(time.time()))
    expires = Column(Float, nullable=False,
        default=lambda: int(time.time()) + 1200000)

    def create(self, user):
        self.token = str(uuid.uuid1())
        self.user_id = user.id
        return self

    def refresh_token(self):
        if self.expires >= int(time.time()):
            expires = int(time.time() + 1200000)

    
class Backlink(Base):
    __tablename__ = 'backlinks'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer,
        ForeignKey('leaves.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    target_id = Column(Integer,
        ForeignKey('leaves.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

class Leaf(Base):
    __tablename__ = 'leaves'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    uri = Column(String(256), unique=True)
    name = Column(String(256))
    date = Column(Float, nullable=False,
        default=lambda: int(time.time()))

    def create(self, uri, name, branch):
        self.parent_id = branch.id
        self.uri = uri
        self.name = name
        self.date = int(time.time())
        return self

    def __repr__(self):
        return '<Leaf {}>'.format(self.title)

class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    uri = Column(String(256))
    name = Column(String(256))
    default_id = Column(Integer)

    def create(self, uri, name, root):
        self.uri = uri
        self.name = name
        self.parent_id = root.id
        return self

    def __repr__(self):
        return '<Branch {}>'.format(self.name)

class Root(Base):
    __tablename__ = 'roots'

    id = Column(Integer, primary_key=True)
    uri = Column(String(256))

    def create(self, uri):
        self.uri = uri
        return self
    
    def __repr__(self):
        return '<Root URL {}>'.format(self.uri)
