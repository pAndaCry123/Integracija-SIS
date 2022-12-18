import pandas as pd
import numpy as np


def impute(df, col_name):
    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 5:ind + 5].dropna()
            df[col_name][ind] = temp.mean()


def above(df, col_name):
    for ind in df.index:
        if df[col_name][ind] > 100:
            temp = df[col_name].iloc[ind - 10:ind - 1].mean()
            df[col_name][ind] = temp


def get_data(frame_data):
    frame_data['datetime'] = pd.to_datetime(frame_data['datetime'])
    columns = ['temp', 'humidity', 'windgust', 'windspeed', 'sealevelpressure', 'cloudcover', 'visibility']

    for col in columns:
        impute(frame_data, col)

    above(frame_data, 'temp')

    return frame_data


if __name__ == '__main__':
    data_frame = pd.read_csv(
        '../Training Data/NYS Weather Data/New York City, NY/New York City, ... 2018-01-01 to 2018-12-31.csv')
    data = data_frame[
        ['datetime', 'temp', 'humidity', 'windgust', 'windspeed', 'sealevelpressure', 'cloudcover', 'visibility',
         'conditions']]
    data = get_data(data)

    print(data)
