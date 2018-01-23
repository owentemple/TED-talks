import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def read_data():
    df = pd.read_excel(os.path.join('..', settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

def cross_validate(df):
    clf = LinearRegression()

    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    print("Predictors: {}".format(predictors))
    predictions = cross_validation.cross_val_predict(clf, df[predictors], df[settings.TARGET], cv=settings.CV_FOLDS)

    return predictions

def compute_error(target, predictions):
    return mean_squared_error(target, predictions)

def create_test_set(df):
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    X_train, X_test, y_train, y_test = train_test_split(df[predictors], df[settings.TARGET], random_state = 42)
    return X_train, X_test, y_train, y_test

def create_summary(X_train, y_train):
    X = X_train
    X2 = sm.add_constant(X)
    est = sm.OLS(y_train, X2)
    est2 = est.fit()
    print(est2.summary())

if __name__ == "__main__":
    df = read_data()
    X_train, X_test, y_train, y_test = create_test_set(df)
    create_summary(X_train, y_train)
    predictions = cross_validate(df)
    error = compute_error(df[settings.TARGET], predictions)
    print("Mean Squared Error: {}".format(error))