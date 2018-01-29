import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
import ast
import re

# Read in the data
def read_data():
    df = pd.read_excel(os.path.join('..', settings.PROCESSED_DIR, "all.xls"), encoding="ISO-8859-1")
    df = df.reset_index()
    return df

# Adds transcripts for 4 talks whose transcripts exceed maximum csv single cell capacity of 32767 characters
def add_long_transcripts(df):
    long_transcripts = {354: 'dan_gilbert_researches_happiness.txt', \
                        2441: 'elon_musk_the_future_we_re_building_and_boring.txt', \
                        2421: 'gretchen_carlson_david_brooks_political_common_ground_in_a_polarized_united_states.txt', \
                        2387: 'yuval_noah_harari_nationalism_vs_globalism_the_new_political_divide.txt'}
    for k, v in long_transcripts.items():
        with open(os.path.join('..', settings.DATA_DIR, v)) as file:
            data = file.read()
            data = data.replace('\t', '')
            data = data.replace('\n', '')
            df.at[k, 'transcript'] = data
    return df

# For speakers whose occupation was blank on TED.com, keep row but add 'No Occupation Noted' for speaker
def fill_null_occupations():
    df['speaker_occupation'].fillna('No Occupation Noted', axis=0, inplace=True)

# Because this analysis focuses on individual speaking styles, remove rows with multiple speakers
def remove_multiple_speakers():
    return df[df['num_speaker'] == 1]

# Remove rows and talks that do not have an English transcript posted to TED.com
def drop_no_transcript():
    return df.dropna(axis=0)

# Function used in apply to trim Question and Answer sections off the end of transcripts
# Used below to find the pattern "Chris Anderson:" to show when moderator is questioning or congratulating the speaker
def trim_q_and_a(x, pattern, offset):
    trim_index = x.find(pattern, 400)
    if trim_index == -1:
        return x
    return x[:trim_index+offset]

# Function used in apply to unpack ratings categories from JSON dictionary that was stored in 'ratings' variable on TED.com
def parse_ratings(x, label):
    x = ast.literal_eval(x)
    for row in x:
        if row['name'] == label:
            return int(row['count'])
    else:
        return 0

# Counts the number of times a string pattern occurs in a transcript. Used to find '(Applause)' and '(Laughter)' in transcript
def count_audience_reaction(x, term):
    return x.count(term)

# Drop rows with multiple speakers so that analysis if focused on patterns of talks by individuals
def drop_rows_with_conversations():
    return df[df['conversation'] == 0]

# Drop rows that are primarily musical performances so that final analysis represents a speaking style
def drop_rows_with_music():
    return df[df['music'] == 0]


def create_new_columns():
    # Create columns from ratings
    df['persuasive'] = df['ratings'].apply(parse_ratings, args=('Persuasive',))
    df['inspiring'] = df['ratings'].apply(parse_ratings, args=('Inspiring',))
    df['unconvincing'] = df['ratings'].apply(parse_ratings, args=('Unconvincing',))
    df['applause'] = df['transcript'].apply(count_audience_reaction, args=('(Applause)',))
    df['laughter'] = df['transcript'].apply(count_audience_reaction, args=('(Laughter)',))
    return df

# Normalizes ratings for the number of views to account for the fact that
# higher viewed talks have more opportunity to collect ratings by users
def normalize_for_views():
    df['norm_persuasive'] = df['persuasive'] / df['views']
    df['norm_inspiring'] = df['inspiring'] / df['views']
    df['norm_unconvincing'] = df['unconvincing'] / df['views']
    return df

# Remove occasional parenthetical notations in the transcript so that analysis is measuring words spoken by speaker
def remove_parenthetical(x):
    return re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", x)

# To get a sense for the story structure of talks, these 3 functions can be used to divide transcripts by 2, 3, or 4
def divide_transcript_into_halves(x, n):
    list_x = x.split(" ")
    mid=int((len(list_x) + 1) / 2)
    if n == 1:
        return ' '.join(list_x[:mid])
    if n == 2:
        return ' '.join(list_x[mid:])
    return None

def divide_transcript_into_thirds(x, n):
    list_x = x.split(" ")
    first_third=int((len(list_x) + 1) / 3)
    third_third= 2 * first_third
    if n == 1:
        return ' '.join(list_x[:first_third])
    elif n == 2:
        return ' '.join(list_x[first_third:third_third])
    elif n == 3:
        return ' '.join(list_x[third_third:])
    return None

def divide_transcript_into_quarters(x, n):
    list_x = x.split(" ")
    first_q=int((len(list_x) + 1) / 4)
    second_q = first_q * 2
    third_q = first_q * 3
    if n == 1:
        return ' '.join(list_x[:first_q])
    elif n == 2:
        return ' '.join(list_x[first_q:second_q])
    elif n == 3:
        return ' '.join(list_x[second_q:third_q])
    elif n == 4:
        return ' '.join(list_x[third_q:])
    return None

# This function is used to implement any of the 3 functions above to divide transcript by word counts
def segment_transcript():
    df['transcript_1sthalf'] = df['transcript'].apply(divide_transcript_into_halves, args=(1,))
    df['transcript_2ndhalf'] = df['transcript'].apply(divide_transcript_into_halves, args=(2,))
    df['transcript_1q'] = df['transcript'].apply(divide_transcript_into_quarters, args=(1,))
    df['transcript_2q'] = df['transcript'].apply(divide_transcript_into_quarters, args=(2,))
    df['transcript_3q'] = df['transcript'].apply(divide_transcript_into_quarters, args=(3,))
    df['transcript_4q'] = df['transcript'].apply(divide_transcript_into_quarters, args=(4,))
    return df

# Writes results of this script to 'processed' folder
def write():
    df.to_excel(os.path.join('..', settings.PROCESSED_DIR, "all_after_annotate.xls"), encoding="ISO-8859-1")


if __name__ == "__main__":
    df = read_data()
    df = add_long_transcripts(df)
    fill_null_occupations()
    df = remove_multiple_speakers()
    df = drop_no_transcript()
    # Removes the Q and A session from end of transcripts
    df['transcript'] = df['transcript'].apply(trim_q_and_a, args=('(Applause)Chris Anderson:', 10))
    df['transcript'] = df['transcript'].apply(trim_q_and_a, args=('(Applause) Chris Anderson:', 10))

    # Reimport dataframe after cleaning transcript and adding 2 new columns manually
    df = pd.read_excel(os.path.join('..', settings.PROCESSED_DIR, "all_with_transcript_edited.xls"), encoding="ISO-8859-1")
    df = drop_rows_with_conversations()
    df = drop_rows_with_music()
    df = create_new_columns()
    df = normalize_for_views()
    df['transcript'] = df['transcript'].apply(remove_parenthetical)
    df = segment_transcript()
    write()


