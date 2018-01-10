import os
import settings
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def read_data():
    train = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return train

def cross_validate(train):
    clf = LinearRegression()

    predictors = train.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]

    predictions = cross_validation.cross_val_predict(clf, train[predictors], train[settings.TARGET], cv=settings.CV_FOLDS)
    return predictions

def compute_error(target, predictions):
    return mean_squared_error(target, predictions)




if __name__ == "__main__":
    train = read_data()
    predictions = cross_validate(train)
    error = compute_error(train[settings.TARGET], predictions)
    print("Mean Squared Error: {}".format(error))