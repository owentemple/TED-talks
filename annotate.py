import os
import settings
import pandas as pd

def add_long_transcripts():
    '''
    Adds transcripts for 3 talks whose transcripts exceeded csv single cell capacity
    '''
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all.xls"), encoding="ISO-8859-1")
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


if __name__ == "__main__":
    add_long_transcripts()