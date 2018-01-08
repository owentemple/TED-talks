import os
import settings
import pandas as pd

def concatenate():
    '''
    Create joined Excel file of TED Talk's metadata and English transcript
    '''
    files = os.listdir(settings.DATA_DIR)
    meta_df = pd.read_csv(os.path.join(settings.DATA_DIR, 'ted_main.csv'), encoding="ISO-8859-1")
    trans_df = pd.read_csv(os.path.join(settings.DATA_DIR, 'transcripts.csv'), encoding="ISO-8859-1")
    all_df = pd.merge(meta_df, trans_df, how='left', left_on='url', right_on='url')
    all_df.to_excel(os.path.join(settings.PROCESSED_DIR, 'all.xls'), encoding="ISO-8859-1")


if __name__ == "__main__":
    concatenate()