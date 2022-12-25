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
    feels_like = Column(Float)
    humidity = Column(Float)
    wind_gust = Column(Float)
    wind_speed = Column(Float)
    sea_level_pressure = Column(Float)
    cloud_cover = Column(Float)
    visibility = Column(Float)
    condition = Column(Float)
    day_part = Column(Float)
    day = Column(Integer)
    day_week = Column(Integer)
    temp_day = Column(Integer)
    year_part = Column(Float)
    sin_time = Column(Float)
    cos_time = Column(Float)
    day_sin = Column(Float)
    day_cos = Column(Float)
    sin_month = Column(Float)
    cos_month = Column(Float)
    yesterday_load = Column(Float)
    mean_load = Column(Float)
    load = Column(Float)


    def __init__(self, **kwargs):

        self.time_stamp = datetime.datetime.strptime(kwargs['Time Stamp'],'%Y-%m-%d %H:%M:%S')
        self.temperature =round(float(kwargs['temp']), 2)
        self.feels_like =round(float(kwargs['feelslike']), 2)
        self.humidity = round(float(kwargs['humidity']), 2)
        self.wind_gust = round(float(kwargs['windgust']), 2)
        self.wind_speed = round(float(kwargs['windspeed']), 2)
        self.sea_level_pressure = round(float(kwargs['sealevelpressure']), 2)
        self.cloud_cover = round(float(kwargs['cloudcover']), 2)
        self.visibility = round(float(kwargs['visibility']), 2)
        temp = kwargs['conditions'].replace(' ', '_').replace(',', '')
        self.condition = round(float(WeatherType[temp].value), 2)
        self.day_part = round(float(kwargs['day_part']), 2)
        self.day = int(kwargs['day'])
        self.day_week = int(kwargs['day_week'])
        self.temp_day = int(kwargs['temp_day'])
        self.year_part = round(float(kwargs['year_part']), 2)
        self.sin_time = round(float(kwargs['sin_time']), 2)
        self.cos_time = round(float(kwargs['cos_time']), 2)
        self.day_sin = round(float(kwargs['cos_time']), 3)
        self.day_cos = round(float(kwargs['cos_time']) ,3)
        self.sin_month = round(float(kwargs['sin_month']), 3)
        self.cos_month = round(float(kwargs['cos_month']), 3)
        self.yesterday_load = round(float(kwargs['yesterday_load']), 2)
        self.mean_load = round(float(kwargs['Mean Load']), 2)
        self.load = round(float(kwargs['Load']), 2)

def impute(df, col_name):
    import numpy as np
    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 15:ind + 15].dropna()
            df[col_name][ind] = temp.mean()

def return_all_elements():
    #weathers = session.query(Weather).all()
    import pandas as pd
    res = pd.read_sql_table('weather',db).drop(['id','time_stamp'], axis=1)

    impute(res,'wind_gust')
    impute(res,'load')
    impute(res,'yesterday_load')
    impute(res,'humidity')
    return res


def store_to_database(model):
    session.add(model)
    session.commit()


if __name__ == "__main__":
    base.metadata.create_all(db)