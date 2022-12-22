import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

db_string = "postgresql://postgres:test@localhost:5432"

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()



class WeatherType(enum.Enum):
    Rain = 0
    Rain_Overcast = 0.12
    Rain_Partially_cloudy = 0.24
    Partially_cloudy = 0.36
    Clear = 0.48
    Snow = 0.6
    Snow_Partially_cloudy = 0.72
    Snow_Overcast = 0.84
    Overcast = 0.96


class Weather(base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_gust = Column(Float)
    wind_speed = Column(Float)
    sea_level_pressure = Column(Float)
    cloud_cover = Column(Float)
    visibility = Column(Float)
    condition = Column(Float)
    load = Column(Float)


    def __init__(self, **kwargs):

        self.time_stamp = datetime.datetime.strptime(kwargs['Time Stamp'],'%Y-%m-%d %H:%M:%S')
        self.temperature = float(kwargs['temp'])
        self.humidity = float(kwargs['humidity'])
        self.wind_gust = float(kwargs['windgust'])
        self.wind_speed = float(kwargs['windspeed'])
        self.sea_level_pressure = float(kwargs['sealevelpressure'])
        self.cloud_cover = float(kwargs['cloudcover'])
        self.visibility = float(kwargs['visibility'])
        temp = kwargs['conditions'].replace(' ', '_').replace(',', '')
        self.condition = float(WeatherType[temp].value)
        self.load = float(kwargs['Load'])






def store_to_database(model):
    session.add(model)
    session.commit()


if __name__ == "__main__":
    base.metadata.create_all(db)