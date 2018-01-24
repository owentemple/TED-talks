import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
import numpy as np
from scipy.spatial import distance


def read_data():
    df = pd.read_excel(os.path.join('..',settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

def find_similar_speaker(name):
    numerical = df.select_dtypes(include=['int64','float64'])
    df_normalized = (numerical - numerical.mean()) / numerical.std()
    df_normalized.drop(['conversation','music','index','languages','comments', 'duration', 'views','persuasive', 'unconvincing', 'inspiring', 'film_date', 'published_date','published_year','AllPunc','Period','Comma','Colon','SemiC','QMark','Exclam','Dash','Quote','Apostro','Parenth','OtherP', 'affect_1h','posemo_1h','negemo_1h', 'anx_1h', 'anger_1h', 'sad_1h', 'affect_2h', 'posemo_2h', 'negemo_2h', 'anx_2h', 'anger_2h', 'sad_2h', 'affect_1q', 'posemo_1q', 'negemo_1q', 'anx_1q', 'anger_1q', 'sad_1q', 'affect_2q', 'posemo_2q', 'negemo_2q', 'anx_2q', 'anger_2q', 'sad_2q', 'affect_3q', 'posemo_3q', 'negemo_3q', 'anx_3q', 'anger_3q', 'sad_3q', 'affect_4q', 'posemo_4q','negemo_4q', 'anx_4q', 'anger_4q','sad_4q','posemo_change_h', 'negemo_change_h','affect_change_h', 'posemo_change_q', 'negemo_change_q', 'affect_change_q'],axis=1,inplace=True)
    speaker_normalized = df_normalized[df["main_speaker"] == name]
    speaker_normalized = speaker_normalized.iloc[0]
    euclidean_distances = df_normalized.apply(lambda row: distance.euclidean(row, speaker_normalized), axis=1)
    second_smallest_value = euclidean_distances.nsmallest(2).iloc[1]
    rec_idx = euclidean_distances[euclidean_distances == second_smallest_value].index
    print(df[['main_speaker', 'url']].iloc[rec_idx])
    return df[['main_speaker', 'description', 'url' ]].iloc[rec_idx]


if __name__ == "__main__":
    df = read_data()
    find_similar_speaker("Al Gore")