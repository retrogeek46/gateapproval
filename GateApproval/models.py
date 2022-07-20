from sqlalchemy import Column, Integer, String
from GateApproval.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    role = Column(String(10))
    password = Column(String(256))

    def __init__(self, name=None, email=None, role=None, password=None):
        self.name = name
        self.email = email
        self.role = role
        self.password = password
        

    def __repr__(self):
        return '<User %r>' % (self.name)


class Visitor(Base):
    __tablename__ = 'visitors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    document_img_path = Column(String(500))
    visitor_img_path = Column(String(500))

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Visitor %r>' % (self.name)