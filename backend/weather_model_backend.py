import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

db_string = "postgresql://postgres:test@localhost:5432/isis"

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
    last_hour_temperature = Column(Float)
    yesterday_temperature = Column(Float)
    #day_bef_yesterday_temperature = Column(Float)
    #diff_temp = Column(Float)
    #mean_temp = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Float)
    wind_gust = Column(Float)
    wind_speed = Column(Float)
    #wind_dir = Column(Float)
    sea_level_pressure = Column(Float)
    cloud_cover = Column(Float)
    visibility = Column(Float)
    condition = Column(Float)
    day_part = Column(Float)
    day = Column(Integer)
    corona = Column(Integer)
    day_week = Column(Integer)
    temp_day = Column(Integer)
    #year_part = Column(Float)
    sin_time = Column(Float)
    cos_time = Column(Float)
    #day_sin = Column(Float)
    #day_cos = Column(Float)
    #sin_month = Column(Float)
    #cos_month = Column(Float)
    #diff_load = Column(Float)
    #yesterday_temp = Column(Float)
    #yesterday_load = Column(Float)
    #mean_load = Column(Float)
    last_hour_load = Column(Float)
    load = Column(Float)


    def __init__(self, **kwargs):

        self.time_stamp = datetime.datetime.strptime(kwargs['Time Stamp'],'%Y-%m-%d %H:%M:%S')
        self.temperature =round(float(kwargs['temp']), 2)
        self.last_hour_temperature =round(float(kwargs['last_hour_temperature']), 2)
        self.yesterday_temperature =round(float(kwargs['yesterday_temperature']), 2)
        #self.day_bef_yesterday_temperature =round(float(kwargs['day_bef_yesterday_temperature']), 2)
        #self.diff_temp =round(float(kwargs['diff_temp']), 2)
        #self.mean_temp =round(float(kwargs['Mean Temp']), 2)
        self.feels_like =round(float(kwargs['feelslike']), 2)
        self.humidity = round(float(kwargs['humidity']), 2)
        self.wind_gust = round(float(kwargs['windgust']), 2)
        self.wind_speed = round(float(kwargs['windspeed']), 2)
        #self.wind_dir = round(float(kwargs['winddir']), 2)
        self.sea_level_pressure = round(float(kwargs['sealevelpressure']), 2)
        self.cloud_cover = round(float(kwargs['cloudcover']), 2)
        self.visibility = round(float(kwargs['visibility']), 2)
        temp = kwargs['conditions'].replace(' ', '_').replace(',', '')
        self.condition = round(float(WeatherType[temp].value), 2)
        self.day_part = round(float(kwargs['day_part']), 2)
        self.day = int(kwargs['day'])
        self.corona = int(kwargs['corona'])
        self.day_week = int(kwargs['day_week'])
        self.temp_day = int(kwargs['temp_day'])
        #self.year_part = round(float(kwargs['year_part']), 2)
        self.sin_time = round(float(kwargs['sin_time']), 2)
        self.cos_time = round(float(kwargs['cos_time']), 2)
        #self.day_sin = round(float(kwargs['cos_time']), 3)
        #self.day_cos = round(float(kwargs['cos_time']) ,3)
        #self.sin_month = round(float(kwargs['sin_month']), 3)
        #self.cos_month = round(float(kwargs['cos_month']), 3)
        #self.yesterday_temp = round(float(kwargs['yesterday_temp']), 2)
        #self.yesterday_load = round(float(kwargs['yesterday_load']), 2)
        #self.diff_load = round(float(kwargs['diff_load']), 2)
        #self.mean_load = round(float(kwargs['Mean Load']), 2)
        self.last_hour_load = round(float(kwargs['last_hour_load']), 2)
        self.load = round(float(kwargs['Load']), 2)

def impute(df, col_name):
    import numpy as np



    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind:ind + 5].dropna()
            df[col_name][ind] = temp.mean()

    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind-5:ind].dropna()
            df[col_name][ind] = temp.mean()

    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind-5:ind + 5].dropna()
            df[col_name][ind] = temp.mean()



def return_all_elements():
    #weathers = session.query(Weather).all()
    res = pd.read_sql_table('weather',db).drop(['id','time_stamp'], axis=1)
    #res = return_elements_from_database_in_range_corona(datetime.date(2020,5,1), datetime.date(2021,9,3))
    temp_offeset = pd.read_sql_table('weather_test',db).drop(['id','time_stamp'], axis=1)
    min_temp, max_temp = return_min_max_temp(temp_offeset)

    res = res[res['temperature'] >= min_temp]
    res = res[res['temperature'] <= max_temp]
    #res = res[res['corona'] == 1]

    impute(res,'wind_gust')
    impute(res,'wind_gust')
    impute(res,'load')
    impute(res,'last_hour_load')
    impute(res,'last_hour_load')
    impute(res,'yesterday_temperature')
    impute(res,'yesterday_temperature')
    impute(res,'last_hour_temperature')
    impute(res,'last_hour_temperature')
    #impute(res,'yesterday_load')
    #impute(res,'yesterday_temp')
    impute(res,'humidity')
    impute(res,'visibility')
    impute(res,'cloud_cover')
    impute(res,'sea_level_pressure')
    #impute(res,'wind_dir')
    #impute(res,'mean_temp')
    #impute(res,'diff_temp')
    #impute(res,'diff_load')
    #res.drop(['corona'], axis=1)
    print('asda-----------------------dasdas')
    print(res['wind_gust'].isnull().any())
    print(res['last_hour_load'].isnull().any())
    print(res['yesterday_temperature'].isnull().any())
    print(res['humidity'].isnull().any())
    print(res['visibility'].isnull().any())
    print(res['cloud_cover'].isnull().any())

    return res


def return_min_max_temp(dataframe):
    return  min(dataframe['temperature']), max(dataframe['temperature'])

def return_elements_from_database_in_range(start_date,end_date):
    res = pd.read_sql_table('weather', db)
    impute(res, 'wind_gust')
    impute(res, 'load')
    #impute(res, 'yesterday_load')
    #impute(res, 'yesterday_temp')
    impute(res, 'humidity')
    res['date'] = pd.to_datetime(res['time_stamp']).dt.date
    res = res[(res['date'] >= start_date) & (res['date'] <= end_date)]
    res = res.drop(['id', 'time_stamp','date'], axis=1)
    return res


def return_elements_from_database_in_range_corona(start_date,end_date):
    res = pd.read_sql_table('weather', db)
    res['date'] = pd.to_datetime(res['time_stamp']).dt.date
    res = res[(res['date'] >= start_date) & (res['date'] <= end_date)]
    res = res.drop(['id', 'time_stamp','date'], axis=1)
    return res


def return_min_max_load():
    res = pd.read_sql_table('weather', db)
    data = res['load']
    return min(data) , max(data)

def store_to_database(model):
    session.add(model)
    session.commit()


if __name__ == "__main__":
    base.metadata.create_all(db)