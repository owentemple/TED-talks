import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression


def read_data():
    df = pd.read_excel(os.path.join('..', settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df


def create_summary_persuasive(df):
    lr = LinearRegression()
    predictors = ['i', 'negate','anx_1q','posemo_2q','interrog','negemo','risk', 'see', 'money', 'Moral', 'focuspresent', 'quant']
    lr.fit(df[predictors], df['norm_persuasive'])

    X = df[predictors]
    X2 = sm.add_constant(X)
    est = sm.OLS(df['norm_persuasive'], X2)
    est2 = est.fit()
    print(est2.summary())
    pass

def create_summary_inspiring(df):
    lr = LinearRegression()
    predictors = ['we','i','social','sad_2q','relig','achieve','power', 'focusfuture', ]
    lr.fit(df[predictors], df['norm_inspiring'])

    X = df[predictors]
    X2 = sm.add_constant(X)
    est = sm.OLS(df['norm_inspiring'], X2)
    est2 = est.fit()
    print(est2.summary())


if __name__ == "__main__":
    df = read_data()
    create_summary_persuasive(df)
    create_summary_inspiring(df)
