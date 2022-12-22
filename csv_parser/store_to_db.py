from models import Weather, store_to_database
import pandas as pd
from numpy import  nan

def return_data_frame(path: str) -> pd.DataFrame:
    data_frame = pd.read_csv(path)
    return data_frame


def load_to_database(data_frame):
    last_condition = ''
    for index, row in data_frame.iterrows():
        #logic to change conditions where is null
        row_dict = row.to_dict()
        if row_dict['conditions'] is nan:
            row_dict['conditions'] = last_condition

        w = Weather(**row_dict)
        store_to_database(w)
        last_condition = row_dict['conditions']





if __name__ == '__main__':

    list_years = ['2018','2019','2020','2021']
    for item in list_years:
        data = return_data_frame('packed_data_{}.csv'.format(item))
        load_to_database(data)