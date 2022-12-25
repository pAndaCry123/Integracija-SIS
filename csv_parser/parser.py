import pandas as pd
import numpy as np
import os

def impute(df, col_name):
    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 5:ind + 20].dropna()
            df[col_name][ind] = temp.mean()


def above(df, col_name):
    for ind in df.index:
        if abs(df[col_name][ind]) > 60:
            temp = df[col_name].iloc[ind - 10:ind - 1].mean()
            df[col_name][ind] = temp


def get_data(frame_data):
    frame_data['datetime'] = pd.to_datetime(frame_data['datetime'])
    columns = ['temp', 'humidity', 'feelslike', 'windgust', 'windspeed', 'sealevelpressure', 'cloudcover', 'visibility']

    for col in columns:
        impute(frame_data, col)

    above(frame_data, 'temp')
    above(frame_data, 'feelslike')
    return frame_data


def cover_loads_for_explicit_year(data, directory,year):
    ind = 0
    lista = []

    for list in os.listdir(directory):
        if year not in list:
            continue

        for list_csv in os.listdir(directory + '\\' + list):
            place = directory + '\\' + list + '\\' + list_csv
            if year not in place:
                continue
            data_frame1 = pd.read_csv(directory + '\\' + list + '\\' + list_csv)
            data_frame1['Time Stamp'] = pd.to_datetime(data_frame1['Time Stamp'])
            data_frame1['Time Stamp'] = data_frame1['Time Stamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
            data_frame1['Time Stamp'] = pd.to_datetime(data_frame1['Time Stamp'],format='%Y-%m-%dT%H:%M:%S')

            data1 = function_to_better_cover(data_frame1)

            temp  = pd.merge(data, data1, on ='Time Stamp')
            lista.append(temp)
            ind += 1

    return  pd.concat(lista)


def function_to_better_cover(data_frame1):
    data1 = data_frame1[data_frame1['Name'] == 'N.Y.C.']
    m = (data1['Time Stamp'].dt.minute == 0) & (data1['Time Stamp'].dt.second == 0)
    return data1[m]


def loop_through_years(years):

    for year in years:
        path_year = '../Training Data/NYS Weather Data/New York City, NY/New York City, ... {}-01-01 to {}-12-31.csv'.format(year,year)
        data_frame = pd.read_csv(path_year)
        data = data_frame[
            ['datetime', 'temp', 'feelslike', 'humidity', 'windgust', 'windspeed', 'sealevelpressure', 'cloudcover', 'visibility',
             'conditions']]
        data = get_data(data)
        data = data.rename(columns={'datetime' : 'Time Stamp'})
        directory = r"C:\Users\petar\Desktop\ISIS\Training Data\NYS Load  Data"
        data['Time Stamp'] = pd.to_datetime(data['Time Stamp'], format='%Y-%m-%dT%H:%M:%S')

        result_for_year = cover_loads_for_explicit_year(data,directory,year)
        result_for_year.to_csv('packed_data_{}.csv'.format(year))


if __name__ == '__main__':

    list_years = ['2018','2019','2020','2021']
    loop_through_years(list_years)






