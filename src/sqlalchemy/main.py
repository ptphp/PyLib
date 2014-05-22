#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2
@author: Joseph
'''
from sqlalchemy.orm import sessionmaker #@UnresolvedImport
from sqlalchemy import create_engine #@UnresolvedImport
from User import User
from sqlalchemy.ext.declarative import declarative_base #@UnresolvedImport
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

if __name__ == '__main__':
    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    ed_user = User('ed', 'Ed Jones', 'edspassword')
    print ed_user
    session = Session()
    session.add(ed_user)
    
    our_user = session.query(User).filter_by(name='ed').first() 
    print our_user