from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import credentials


metadata = MetaData()
Base = declarative_base()
# url = dialect + '://' + user + ':' + paswd + '@' + server + ":" + port + '/android_backend'
# engine = create_engine(url)
# session = sessionmaker()
# session.configure(bind=engine)
# Session = session()


class CloudDB:

    user = credentials.user
    paswd = credentials.passwd
    dialect = 'mysql+pymysql' # db_type + python_driver
    server = ''
    port = '3306'
    db = 'android_backend' # database created via googles UI

    def __init__(self):
        self.metadata = metadata
        self.base = declarative_base()
        self.url = self.dialect + '://' + self.user + ':' + self.paswd + '@' + self.server + ":" + self.port + '/' + self.db
        self.engine = create_engine(self.url)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.Session = session()


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

    # def __init__(self, lat, lon, dictionary_in):
    #     ''' Constructor for inserting data into the Location table in the database
    #         Takes in a location key from our JSON file, and a corresponding dictionary to that key
    #         and creates a row in the data base. You would then need to call SQLAlchemy to insert that row into the database and commit()
    #     '''
    #     self.latitude = lat
    #     self.longitude = lon
    #     self.assaults = dictionary_in['ASSAULT']
    #     self.murders = dictionary_in['MURDER']
    #     self.thefts = dictionary_in['THEFT']
    #     self.rapes = dictionary_in['RAPE']
    #     self.gta = dictionary_in['GTA']
    #     self.robberies = dictionary_in['ROBBERY']
    #     self.other = dictionary_in['OTHER']
