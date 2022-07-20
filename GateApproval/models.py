from xmlrpc.client import Boolean
from sqlalchemy import Column, ForeignKey, Integer, String
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
    verifier_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(50))
    approval_status = Column(Integer)
    verification_status = Column(Integer)
    document_img_path = Column(String(500))
    visitor_img_path = Column(String(500))
    
    def __init__(self, name=None, verifier_id=None, approval_status=None, verification_status=None, document_img_path=None, visitor_img_path=None):
        self.name = name
        self.verifier_id = verifier_id
        self.approval_status = approval_status
        self.verification_status = verification_status
        self.document_img_path = document_img_path
        self.visitor_img_path = visitor_img_path

    def __repr__(self):
        return '<Visitor %r>' % (self.name)