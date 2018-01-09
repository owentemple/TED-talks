import os
import settings
import pandas as pd
from scipy.stats import pearsonr

from nltk.stem.snowball import SnowballStemmer

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc.xls"), encoding="ISO-8859-1")
    return df

def calculate_sentiment_change():
    df['posemo_incr'] = df['posemo2'] - df['posemo1']
    df['negemo_decr'] = df['negemo1'] - df['negemo2']
    df['affect_change'] = df['posemo_incr'] - df['negemo_decr']
    return df

def create_variables_with_median_split():
    pass


def create_published_year():
    df['published_date_dt'] = pd.to_datetime(df['published_date'])
    df['published_dt'] = pd.to_datetime(df['published_date'],unit='s')
    df['published_year'] = df['published_dt'].dt.year
    return df

def create_moral_category_from_subsets():
    df['Harm'] = df['HarmVirtue'] + df['HarmVice']
    df['Fairness'] = df['FairnessVirtue'] + df['FairnessVice']
    df['Purity'] = df['PurityVirtue'] + df['PurityVice']
    df['Ingroup'] = df['IngroupVirtue'] + df['IngroupVice']
    df['Authority'] = df['AuthorityVirtue'] + df['AuthorityVice']
    return df


def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues

def plot_moral_words_by_year():
    df.groupby('published_year')['MoralityGeneral'].mean().plot()
    df.groupby('published_year')['Harm'].mean().plot()
    df.groupby('published_year')['Authority'].mean().plot()
    df.groupby('published_year')['Fairness'].mean().plot()
    df.groupby('published_year')['Ingroup'].mean().plot()
    df.groupby('published_year')['Purity'].mean().plot()

def correlation_and_pvalue_of_moral_words_over_time():
    # Show correlation matrix of moral category by year
    df[['MoralityGeneral', 'Harm', 'Authority', 'Ingroup', 'Purity', 'Fairness', 'published_date']].corr()
    # Show p-value of correlation of moral category by year
    moral_df = df[['MoralityGeneral', 'Harm', 'Authority', 'Ingroup', 'Purity', 'Fairness', 'published_date']]
    calculate_pvalues(moral_df)


if __name__ == "__main__":
    df = read_data()
    df = calculate_sentiment_change()
    df = create_published_year()
    df = create_moral_category_from_subsets()
    plot_moral_words_by_year()
