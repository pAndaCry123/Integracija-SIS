from models import Weather, store_to_database
import pandas as pd
from numpy import nan, isnan, pi, sin, cos

def return_data_frame(path: str) -> pd.DataFrame:
    data_frame = pd.read_csv(path)
    return data_frame


def load_to_database(data_frame):
    '''Function store to database cover again if there is nan values and replace them with last value
    element before that element
    add some attributes like is month in some season
    when some is bigger loss and when some temp conditions
    if we are between 10 and 30 there is less loss couse we dont need heating or air condition
    above or less we need some external party
    '''
    data = data_frame

    last_condition, last_load, feelslike, windgust, yesterday_load = "", 0, 0, 0, 0
    list_hours = [0,1,2,3,4,5,6,7,22,23]
    winter_months =[12,1,2]
    spring_months =[3,4,5]
    summer_months =[6,7,8]
    autumn_months =[9,10,11]

    for index, row in data.iterrows():
        #logic to change conditions where is null
        row_dict = row.to_dict()
        #if something is nan from data set cover that
        if row_dict['windgust'] is nan:
            row_dict['windgust'] = windgust
        if row_dict['conditions'] is nan:
            row_dict['conditions'] = last_condition
        if row_dict['Load'] is nan:
            row_dict['Load'] = last_load
        if row_dict['feelslike'] is nan:
            row_dict['feelslike'] = feelslike
        if pd.to_datetime(row_dict['Time Stamp']).hour in list_hours:
            row_dict['day_part'] = 0
        if pd.to_datetime(row_dict['Time Stamp']).hour not in list_hours:
            row_dict['day_part'] = 1
        #year part :D
        if row['Date'].month in winter_months:
            row_dict['year_part'] = 0
        if row['Date'].month in spring_months:
            row_dict['year_part'] = 0.25
        if row['Date'].month in summer_months:
            row_dict['year_part'] = 0.5
        if row['Date'].month in autumn_months:
            row_dict['year_part'] = 1
        #temperature offset
        if row_dict['temp'] <= 10 or row_dict['temp'] >= 30:
            row_dict['temp_day'] = 1
        if row_dict['temp'] > 10 and row_dict['temp'] < 30:
            row_dict['temp_day'] = 0
        #cover yesterday load if is nan
        if row_dict['yesterday_load'] is nan:
            row_dict['yesterday_load'] = yesterday_load

        w = Weather(**row_dict)
        store_to_database(w)

        last_condition, last_load, feelslike, windgust, yesterday_load =\
            row_dict['conditions'] , row_dict['Load'], row_dict['feelslike'] , row_dict['windgust'] ,row_dict['yesterday_load']


def working_day(frame , year):
    '''Function decide is day working or weekend/
    give days numerations from 1 - 7
    and simple like function belove
    every day repeats in month so we make day sin / cos
    '''
    help = frame
    help = help.groupby('Date').mean()
    help = help.drop(['temp', 'humidity', 'feelslike', 'windgust', 'windspeed', 'sealevelpressure',
                      'cloudcover', 'visibility','Unnamed: 0', 'PTID'], axis =1)
    help['day'] = 0
    help['day_week'] = 0
    help['day_sin'] = 0
    help['day_cos'] = 0
    counter = 1
    if year is '2019':
        counter = 2
    if year is '2020':
        counter = 3
    if year is '2021':
        counter = 3

    week_days = 0

    for index in range(len(help)):
        day = 1
        if counter % 6 == 0:
            day = 0
        if counter % 7 == 0:
            counter = 0
            day = 0
        if week_days %7 == 0:
            week_days = 0

        counter += 1

        help['day'][index] = day
        help['day_week'][index] = week_days
        help['day_sin'][index] = sin(2 * pi * week_days / 7)
        help['day_cos'][index] = cos(2 * pi * week_days / 7)

        week_days += 1


    help['yesterday_load'] = help.Load.shift(-1)

    help = help.rename(columns = {'Load':'Mean Load'})

    frame = pd.merge(frame , help , on='Date')

    return frame


def add_sin_cos_time_cicrle(data_frame):
    '''Adding sin / cos to hours and months couse when we make sin and cos
    together make circular things and network can understand that thoose meanings repeat
    '''

    hours = 24
    months = 12

    data_frame['sin_time'] = sin(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.hour / hours)
    data_frame['cos_time'] = cos(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.hour / hours)

    data_frame['sin_month'] = sin(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.month / months)
    data_frame['cos_month'] = cos(2 * pi * pd.to_datetime(data_frame['Time Stamp']).dt.month / months)

    return data_frame


def impute(df, col_name):
    '''Function whic covers nan values'''

    for ind in df.index:
        if isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 5:ind].dropna()
            df[col_name][ind] = temp.mean()

    return  df

def exclude_holidays(data_frame):
    '''Exclude holidays from dataset'''

    holiday_frame = pd.read_excel('../Training Data/US Holidays 2018-2021.xlsx')
    data_frame['Date'] = pd.to_datetime(data_frame['Time Stamp'] ,format='%Y-%m-%d').dt.date
    holiday_frame['Date'] = pd.to_datetime(holiday_frame['Unnamed: 2']).dt.date
    data_frame = data_frame[~(data_frame['Date'].isin(holiday_frame['Date']))]

    return data_frame

def impute_data_dataset(data):
    ''' Replace null or nan values with mean value'''

    columns = ['temp', 'humidity', 'feelslike', 'windgust', 'windspeed', 'sealevelpressure', 'cloudcover',
               'visibility', 'Load']

    for item in columns:
        data = impute(data, item)

    return  data


if __name__ == '__main__':

    list_years = ['2018','2019','2020','2021']
    for item in list_years:
        data = return_data_frame('packed_data_{}.csv'.format(item))
        data['Date'] = pd.to_datetime(data['Time Stamp'], format='%Y-%m-%d').dt.date

        data = impute_data_dataset(data)

        data= working_day(data, item)
        frame = exclude_holidays(data)
        frame = add_sin_cos_time_cicrle(frame)
        load_to_database(frame)