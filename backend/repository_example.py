import datetime
import csv
import time
import pandas as pd
from csv_parser.weather_model import return_elements_from_database_in_range,return_elements_from_database_in_range_predict
from backend.weather_model_backend import return_all_elements
from csv_parser.store_to_db import load_dataframe_to_database
from csv_parser.parser import loop_through_year
from datetime import date, timedelta
from neural_network.custom_preparer import CustomPreparer
from neural_network.ann_regression import AnnRegression
from neural_network.custom_plotting import CustomPloting
from neural_network.scorer import Scorer

NUMBER_OF_COLUMNS = 24
NUMBER_OF_COLUMNS1 = 25
SHARE_FOR_TRAINING = 0.85

class Repo_example:

    @classmethod
    def upload_file_and_store(cls,file):
        data_frame = pd.read_csv(file)
        data_frame = loop_through_year(data_frame)
        data = load_dataframe_to_database(data_frame)

        return True

    @classmethod
    def train_data(cls,start_date : date,end_date:date):

        #videti da koja baza se koristi
        elements = return_all_elements()
        preparer = CustomPreparer(elements, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING);
        trainX, trainY, testX, testY = preparer.prepare_for_training()
        # make predictions

        ann_regression = AnnRegression()

        ann_regression.compile_fit_predict(trainX, trainY)

        return True

    @classmethod
    def predict_data(cls,start_date :date,days):
        if days > 6:
            return False



        end_date = start_date + timedelta(days - 1)
        elements = return_elements_from_database_in_range_predict(start_date, end_date)
        preparer = CustomPreparer(elements, NUMBER_OF_COLUMNS, 0)
        testX, testY = preparer.prepare_to_predict()
        # make predictions
        ann_regression = AnnRegression()
        testPredict  = ann_regression.compile_fit_predict_with_current_model(testX)

        testPredict, testY = preparer.inverse_transform_plot(testPredict)
        #print(testPredict)
        #print(testY)
        #
        '''preparer = CustomPreparer(elements, NUMBER_OF_COLUMNS, 0)
        trainX, trainY, testX, testY = preparer.prepare_for_training()
        # make predictions

        ann_regression = AnnRegression()
        time_begin = time.time()
        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
        time_end = time.time()
        print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

        # invert predictions
        trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)'''

        # calculate root mean squared error
        scorer = Scorer()
        testScore = scorer.get_absolute_test_score(testY, testPredict)
        print('Test Score: %.2f RAMSE' % (testScore))

        # plotting
        custom_plotting = CustomPloting()
        custom_plotting.show_plots(testPredict, testY)
        cls.store_to_csv(testPredict, start_date, days)
        return testPredict


    @classmethod
    def store_to_csv(cls, testPredict, start_date:datetime.date, days):
        ret_dict = {'date time': [] , 'load' : []}
        counter = 0
        date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
        for days in range(days):
            #date = date + timedelta(days=1)

            for hours in range(24):

                ret_dict['date time'].append(date.strftime('%Y-%m-%d %H:%M:%S'))
                ret_dict['load'].append(testPredict[counter])
                date = date + timedelta(hours=1)
                counter += 1

        df = pd.DataFrame(ret_dict)
        df.to_csv('predicted_values.csv')

