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
    latitude = Column(String(20))
    longitude = Column(String(20))
    assaults = Column(Integer)
    murders = Column(Integer)
    thefts = Column(Integer)
    rapes = Column(Integer)
    gta = Column(Integer)
    robberies = Column(Integer)
    other = Column(Integer)

    def __init__(self, lat, lon, dictionary_in):
        ''' Constructor for inserting data into the Location table in the database
            Takes in a location key from our JSON file, and a corresponding dictionary to that key
            and creates a row in the data base. You would then need to call SQLAlchemy to insert that row into the database and commit()
        '''
        self.latitude = lat
        self.longitude = lon
        self.assaults = dictionary_in['ASSAULT']
        self.murders = dictionary_in['MURDER']
        self.thefts = dictionary_in['THEFT']
        self.rapes = dictionary_in['RAPE']
        self.gta = dictionary_in['GTA']
        self.robberies = dictionary_in['ROBBERY']
        self.other = dictionary_in['OTHER']


def create_table(engine):
    locs = Table('locations', metadata,
          Column('id',Integer, primary_key=True, autoincrement=True),
          Column('latitude', String),
          Column('longitude', String),
          Column('assaults', Integer),
          Column('murders', Integer),
          Column('thefts', Integer),
          Column('rapes', Integer),
          Column('gta', Integer),
          Column('robberies', Integer),
          Column('other', Integer)
          )

    Base.metadata.create_all(engine)

    return locs

def convert_json_to_db(key ,data, session):

    ''' Takes the latlon key from the JSON file, the data associated with it, and the session from main to create entries into the database. '''

    try:
        lat, lon = key.split('-')
    except:
        print(key)
        return
    lon = float(lon)
    if lon < 0:
        lon *= -1
    lon = str(lon)
    data_to_input = Location(lat, lon, data)
    session.add(data_to_input)
    session.flush()
    session.commit()

def main():

    user = ''
    paswd = ''
    dialect = 'mysql+pymysql' # db_type + python_driver
    server = ''
    port = '3306'
    db = 'android_backend' # database created via googles UI

    url = dialect + '://' + user + ':' + paswd + '@' + server + ":" + port + '/android_backend'
    engine = create_engine(url)
    session = sessionmaker()
    session.configure(bind=engine)
    Session = session()
    locs = create_table(engine)

    with open("json_updated.json") as f:
        json_data = f.read()

    loc_vals = json.loads(json_data)

    for keys in loc_vals:
        convert_json_to_db(keys, loc_vals[keys], Session)



main()

