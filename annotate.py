import os
import settings
import pandas as pd

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all.xls"), encoding="ISO-8859-1")
    df = df.reset_index()
    return df


def add_long_transcripts(df):
    '''
    Adds transcripts for 4 talks whose transcripts exceed max csv single cell capacity of 32767 characters
    '''
    long_transcripts = {354: 'dan_gilbert_researches_happiness.txt', \
                        2441: 'elon_musk_the_future_we_re_building_and_boring.txt', \
                        2421: 'gretchen_carlson_david_brooks_political_common_ground_in_a_polarized_united_states.txt', \
                        2387: 'yuval_noah_harari_nationalism_vs_globalism_the_new_political_divide.txt'}
    for k, v in long_transcripts.items():
        with open(os.path.join(settings.DATA_DIR, v)) as file:
            data = file.read()
            data = data.replace('\t', '')
            data = data.replace('\n', '')
            df.at[k, 'transcript'] = data
    return df

def fill_null_occupations():
    df['speaker_occupation'].fillna('No Occupation Noted', axis=0, inplace=True)

def remove_single_speaker():
    return df[df['num_speaker'] == 1]

def drop_no_transcript():
    return df.dropna(axis=0)


if __name__ == "__main__":
    df = read_data()
    df = add_long_transcripts(df)
    fill_null_occupations()
    df = remove_single_speaker()
    df = drop_no_transcript()
