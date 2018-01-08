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

def remove_multiple_speakers():
    return df[df['num_speaker'] == 1]

def drop_no_transcript():
    return df.dropna(axis=0)

def trim_q_and_a(x, pattern, offset):
    trim_index = x.find(pattern, 400)
    if trim_index == -1:
        return x
    return x[:trim_index+offset]

def parse_ratings(x, label):
    x = ast.literal_eval(x)
    for row in x:
        if row['name'] == label:
            return int(row['count'])
    else:
        return 0


def count_audience_reaction(x, term):
    return x.count(term)

def create_new_columns():
    # Create columns from ratings
    df['persuasive'] = df['ratings'].apply(parse_ratings, args=('Persuasive',))
    df['inspiring'] = df['ratings'].apply(parse_ratings, args=('Inspiring',))
    df['unconvincing'] = df['ratings'].apply(parse_ratings, args=('Unconvincing',))
    df['applause'] = df['transcript'].apply(count_audience_reaction, args=('(Applause)',))
    df['laughter'] = df['transcript'].apply(count_audience_reaction, args=('(Laughter)',))
    return df

def remove_parenthetical(x):
    return re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", x)



if __name__ == "__main__":
    df = read_data()
    df = add_long_transcripts(df)
    fill_null_occupations()
    df = remove_multiple_speakers()
    df = drop_no_transcript()
    # Removes the Q and A session from end of transcripts
    df['transcript'] = df['transcript'].apply(trim_q_and_a, args=('(Applause)Chris Anderson:', 10))
    df['transcript'] = df['trim_transcript'].apply(trim_q_and_a, args=('(Applause) Chris Anderson:', 10))
    ## Reimport dataframe after cleaning transcript and adding 2 new columns manually
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_transcript_edited.xls"), encoding="ISO-8859-1")
    df = create_new_columns()
    df['transcript'] = df['transcript'].apply(remove_parenthetical)


