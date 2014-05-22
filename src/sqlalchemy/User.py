#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2
@author: Joseph
'''
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base #@UnresolvedImport
from sqlalchemy import Column, Integer, String #@UnresolvedImport
from sqlalchemy import create_engine #@UnresolvedImport
from sqlalchemy import Sequence#@UnresolvedImport
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
class User(Base):    
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'),primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
        
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
    
if __name__ == '__main__':
    print sqlalchemy.__version__ #@UndefinedVariable
    print engine.execute("select 1").scalar()
    user = User('joseph','zhou','passwprd')
    print user
    print user.name
    print user.id
    print User
    print User.__table__ 
    print User.__mapper__ 
    Base.metadata.create_all(engine) 