from sqlalchemy import Column, MetaData, String, Integer, Float, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
crime_data_long = Table('crime_data_long', metadata,
  Column('id', Integer, primary_key=True),
  Column('latitude', String),
  Column('longitude', String),
  Column('ASSAULT', Integer),
  Column("MURDER", Integer),
  Column("THEFT", Integer),
  Column("RAPE", Integer),
  Column("GTA", Integer),
  Column("ROBBERY", Integer),
  Column("Other", Integer)
)

# if "ASSAULT" in row[0]:
#   master[s]["ASSAULT"] += 1
# elif "MURDER" in row[0]:
#   master[s]["MURDER"] += 1
# elif "THEFT" in row[0]:
#   master[s]["THEFT"] += 1
# elif "RAPE" in row[0]:
#   master[s]["RAPE"] += 1
# elif "GTA" in row[0]:
#   master[s]["GTA"] += 1
# elif "ROBBERY" in row[0]:
#   master[s]["ROBBERY"] += 1
# else:
#   master[s]["OTHER"] += 1
#

# CREATE TABLE IF NOT EXISTS crimedata (
#     `Description` VARCHAR(44) CHARACTER SET utf8,
#     `ID` VARCHAR(13) CHARACTER SET utf8,
#     `Location` VARCHAR(30) CHARACTER SET utf8,
#     `Sherrifs` VARCHAR(29) CHARACTER SET utf8,
#     `Date` DATETIME
# );

engine = create_engine('mysql:///crime_data.db')

