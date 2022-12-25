# Vezbe iz predmeta Inteligentni softverski infrastrukturni sistemi
# Koriscenje neuronske mreze na primeru predvidjanja cena kuca

import time
from ann_regression import AnnRegression
from custom_plotting import CustomPloting
from custom_preparer import CustomPreparer
from scorer import Scorer
from csv_parser.models import return_all_elements
NUMBER_OF_COLUMNS = 23
SHARE_FOR_TRAINING = 0.85

import  pandas as pd
# load the dataset
#dataframe = pandas.read_csv('housing.csv', engine='python', sep=';', header=None)
elements = return_all_elements()
#elements = elements.drop('mean_load', axis=1)
'''elements = elements[elements['day_part'] == 1]
elements = elements[elements['day'] == 1]'''
'''data = elements
for item in elements.columns:
    nan_in_df = data[item].isnull().values.any()
    # Print the dataframe
    print(nan_in_df)
data = elements.loc[pd.isnull(elements).any(1), :].index.values
print(data)'''

# prepare data
preparer = CustomPreparer(elements, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING);
trainX, trainY, testX, testY = preparer.prepare_for_training()
# make predictions

ann_regression = AnnRegression()
time_begin = time.time();
trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
time_end = time.time()
print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

# invert predictions
trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)

# calculate root mean squared error
scorer = Scorer()
trainScore, testScore = scorer.get_absolute(trainY, trainPredict, testY, testPredict)
print('Train Score: %.2f RMSE' % (trainScore))
print('Test Score: %.2f RMSE' % (testScore))

# plotting
custom_plotting = CustomPloting()
custom_plotting.show_plots(testPredict, testY)