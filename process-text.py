import os
import settings
import pandas as pd

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc.xls"), encoding="ISO-8859-1")
    return df

def calculate_sentiment_change_by_halves():
    df['posemo_change_h'] = df['posemo_2h'] - df['posemo_1h']
    df['negemo_change_h'] = df['negemo_2h'] - df['negemo_1h']
    df['affect_change_h'] = df['posemo_change_h'] - df['negemo_change_h']
    return df

def calculate_sentiment_change_by_quarters():
    df['posemo_change_q'] = df['posemo_4q'] - df['posemo_1q']
    df['negemo_change_q'] = df['negemo_4q'] - df['negemo_1q']
    df['affect_change_q'] = df['posemo_change_q'] - df['negemo_change_q']
    return df

# This function increases the magnitude of the normed features to assist interpretability
def scale_up_normed_features():
    df['norm_persuasive'] = df['norm_persuasive'] * 1000000
    df['norm_inspiring'] = df['norm_inspiring'] * 1000000
    df['norm_unconvincing'] = df['norm_unconvincing'] * 1000000
    return df

def create_published_year():
    df['published_date_dt'] = pd.to_datetime(df['published_date'])
    df['published_dt'] = pd.to_datetime(df['published_date'],unit='s')
    df['published_year'] = df['published_dt'].dt.year
    del df['published_dt']
    del df['published_date_dt']
    return df

def create_moral_category_from_subsets():
    df['Harm'] = df['HarmVirtue'] + df['HarmVice']
    df['Fairness'] = df['FairnessVirtue'] + df['FairnessVice']
    df['Purity'] = df['PurityVirtue'] + df['PurityVice']
    df['Ingroup'] = df['IngroupVirtue'] + df['IngroupVice']
    df['Authority'] = df['AuthorityVirtue'] + df['AuthorityVice']
    return df


def write():
    df.to_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")



if __name__ == "__main__":
    df = read_data()
    df = calculate_sentiment_change_by_halves()
    df = calculate_sentiment_change_by_quarters()
    df = scale_up_normed_features()
    df = create_published_year()
    df = create_moral_category_from_subsets()
    write()
