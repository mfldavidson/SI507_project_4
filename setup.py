from sqlalchemy import Column, ForeignKey, Integer, String, REAL, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
import json, csv

# set up base, session, and engine
Base = declarative_base()

session = scoped_session(sessionmaker())

engine = create_engine('sqlite:///state_parks.sqlite', echo=False)

Base.metadata.bind = engine
session.configure(bind=engine)

# define function to create the database
def init_db():
    Base.metadata.create_all(engine)
    return engine

# define classes/tables
class State(Base):
    __tablename__ = 'States'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    State = Column(String(24), nullable = False)
    Abbr = Column(String(2), nullable = False)
    URL = Column(String(250), nullable = False)
    #Parks = Column(Integer, ForeignKey('Parks.Id'))
    Parks_Rel = relationship('Park',secondary='association',back_populates='State_Rel',lazy='dynamic')

class Park(Base):
    __tablename__ = 'Parks'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(250))
    Type = Column(String(250))
    Descr = Column(String(2000))
    Location = Column(String(250))
    #State = Column(Integer, ForeignKey('States.Id'))
    State_Rel = relationship('State',secondary='association',back_populates='Parks_Rel',lazy='dynamic')

class StateParkAssociation(Base):
    __tablename__ = 'association'
    State_Id = Column(Integer, ForeignKey('States.Id'),primary_key=True)
    Park_Id = Column(Integer, ForeignKey('Parks.Id'),primary_key=True)
    State_Assoc = relationship(State, backref=backref('Parks_Assoc'))
    Park_Assoc = relationship(Park, backref=backref('State_Assoc'))

# create the database
init_db()
