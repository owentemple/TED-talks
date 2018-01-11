import os
import settings
import pandas as pd
import operator

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

def create_test_set(df):
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    X_train, X_test, y_train, y_test = train_test_split(df[predictors], df[settings.TARGET], random_state = 42)
    return X_train, X_test, y_train, y_test


def compute_error(target, predictions):
    return mean_squared_error(target, predictions)

def sort_important_features(X_train, y_train):
    rf = RandomForestRegressor()
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    rf.fit(X_train, y_train)
    predictions = rf.predict(X_train)
    results = {name: score for name, score in zip(predictors, rf.feature_importances_)}
    sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_results)
    accuracy = rf.score(X_train, y_train)
    print("Accuracy: {}".format(accuracy))


if __name__ == "__main__":
    df = read_data()
    X_train, X_test, y_train, y_test = create_test_set(df)
    sort_important_features(X_train, y_train)
    #error = compute_error(train[settings.TARGET], predictions)
    #print("Mean Squared Error: {}".format(error))