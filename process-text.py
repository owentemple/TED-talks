import os
import settings
import pandas as pd

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc.xls"), encoding="ISO-8859-1")
    return df






def calculate_sentiment_change():
    df['posemo_change'] = df['posemo2'] - df['posemo1']
    df['negemo_change'] = df['negemo2'] - df['negemo1']
    df['affect_change'] = df['posemo_change'] + df['negemo_change']
    return df

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





if __name__ == "__main__":
    df = read_data()
    df = calculate_sentiment_change()
    df = create_published_year()
    df = create_moral_category_from_subsets()
    plot_moral_words_by_year()
