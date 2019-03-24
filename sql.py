#!/usr/bin/python3

import json
from sqlalchemy import String, Column, Integer, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

metadata = MetaData()
Base = declarative_base()

class Location(Base):

    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "locations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    location = Column(String(20))
    assaults = Column(Integer)
    murders = Column(Integer)
    thefts = Column(Integer)
    rapes = Column(Integer)
    gta = Column(Integer)
    robberies = Column(Integer)
    other = Column(Integer)

    def __init__(self, key, dictionary_in):
        ''' Constructor for inserting data into the Location table in the database
            Takes in a location key from our JSON file, and a corresponding dictionary to that key
            and creates a row in the data base. You would then need to call SQLAlchemy to insert that row into the database and commit()
        '''
        self.location = key # our current data is stored in key { key:val } pairs so we need to pass in the main key along with the data
        self.assaults = dictionary_in['ASSAULT']
        self.murders = dictionary_in['MURDER']
        self.thefts = dictionary_in['THEFT']
        self.rapes = dictionary_in['RAPE']
        self.gta = dictionary_in['GTA']
        self.robberies = dictionary_in['ROBBERY']
        self.other = dictionary_in['OTHER']

def create_table(engine, session, metadata):
    Table('locations', metadata,
          Column('id',Integer, primary_key=True, autoincrement=True),
          Column('location', String),
          Column('assaults', Integer),
          Column('murders', Integer),
          Column('thefts', Integer),
          Column('rapes', Integer),
          Column('gta', Integer),
          Column('robberies', Integer),
          Column('other', Integer)
          )

    Base.metadata.create_all(engine)

def main():

    url = dialect + '://' + user + ':' + paswd + '@' + server + ":" + port + '/android_backend'
    engine = create_engine(url)
    session = sessionmaker(bind=engine)
    Session = session()
    create_table(engine, Session, metadata)


main()

