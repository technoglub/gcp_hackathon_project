from sqlalchemy import String, Column, Integer, Float, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base

metadata = MetaData()
Base = declarative_base()
# url = dialect + '://' + user + ':' + paswd + '@' + server + ":" + port + '/android_backend'
# engine = create_engine(url)
# session = sessionmaker()
# session.configure(bind=engine)
# Session = session()


def create_table(db):
    locs = Table('user_interface', metadata,
                 Column('id',Integer, primary_key=True, autoincrement=True),
                 Column("date", Date),
                 Column("gta", Integer),
                 Column("assault", Integer),
                 Column("murder", Integer),
                 Column("theft", Integer),
                 Column("sexual_assault", Integer),
                 Column("robbery", Integer),
                 Column("other", Integer),
                 )

    db.metadata.create_all(db.engine)

    return locs

def get_location_schematic():
    data_to_enter = dict()
    data_to_enter["gta"] = 0
    data_to_enter["assaults"] = 0
    data_to_enter["murders"] = 0
    data_to_enter["thefts"] = 0
    data_to_enter["rapes"] = 0
    data_to_enter["robberies"] = 0
    data_to_enter["other"] = 0
    data_to_enter["date"] = 0
    return data_to_enter


class CloudDB:

    user = ''
    paswd = ''
    dialect = 'mysql+pymysql' # db_type + python_driver
    server = ''
    port = '3306'
    db = 'android_backend' # database created via googles UI

    def __init__(self):
        self.metadata = metadata
        self.base = Base
        self.url = self.dialect + '://' + self.user + ':' + self.paswd + '@' + self.server + ":" + self.port + '/' + self.db
        self.engine = create_engine(self.url, echo=True, pool_recycle=3600)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.Session = session()


    def make_scoped_session(self):

        session = sessionmaker()
        session.configure(bind=self.engine)
        return scoped_session(session)


class Location(Base):

    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "locations2"
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    assaults = Column(Integer)
    murders = Column(Integer)
    thefts = Column(Integer)
    rapes = Column(Integer)
    gta = Column(Integer)
    robberies = Column(Integer)
    other = Column(Integer)


class UserInterface(Base):

    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "user_interface"
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    assaults = Column(Integer)
    murders = Column(Integer)
    thefts = Column(Integer)
    rapes = Column(Integer)
    gta = Column(Integer)
    robberies = Column(Integer)
    other = Column(Integer)

class DatedLocation(Base):
        '''
            This is the main data we store
            Since it's inherited from the sqlalchemy Base class,
            we can access this variable directly to create and store data
        '''

        __tablename__ = "dated_locations"
        id = Column(Integer, autoincrement=True, primary_key=True)
        latitude = Column(Float)
        longitude = Column(Float)
        date = Column(Date)
        assaults = Column(Integer)
        murders = Column(Integer)
        thefts = Column(Integer)
        rapes = Column(Integer)
        gta = Column(Integer)
        robberies = Column(Integer)
        other = Column(Integer)


class MasterCrimeTable(Base):
    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "master_crime_table"
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(Date)
    description = Column(String(40))


def add_data_to_master(new_entry):
    entry = DatedLocation(latitude=new_entry["latitude"], longitude=new_entry["longitude"],
                          date=new_entry["date"], description=new_entry["description"]
                          )
    return entry


def add_data_to_db(new_entry, db):
    data_to_enter = DatedLocation(latitude=new_entry["latitude"], longitude=new_entry["longitude"],
                                  assaults=new_entry['assault'], date=new_entry["date"],
                                  murders=new_entry["murder"], rapes=new_entry["rape"],
                                  thefts=new_entry["theft"], gta=new_entry["gta"],
                                  robberies=new_entry["robbery"], other=new_entry["other"]
                                  )
    return data_to_enter


def feed_master(entry):
    data_to_enter = MasterCrimeTable(latitude=entry["latitude"], longitude=entry["longitude"],
                                     date=entry["date"], description=entry["description"])
    return data_to_enter
<<<<<<< HEAD
=======

>>>>>>> 049dcd18c1aae4abb452121fdfaada8607d0d944
