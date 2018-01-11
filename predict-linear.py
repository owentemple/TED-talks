import os
import settings
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression


def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df


def create_summary(df):
    lr = LinearRegression()
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    lr.fit(df[predictors], df[settings.TARGET])

    X = df[predictors]
    X2 = sm.add_constant(X)
    est = sm.OLS(df[settings.TARGET], X2)
    est2 = est.fit()
    print(est2.summary())

if __name__ == "__main__":
    df = read_data()
    create_summary(df)
