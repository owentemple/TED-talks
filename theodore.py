from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
import os
import settings
import pandas as pd
import numpy as np
from scipy.spatial import distance

app = Flask(__name__)

bookmarks = []
app.config['SECRET_KEY'] = '+\xb3N\xc0\xe90A\x8d1Lv\x87\x13\xf8\xecY\xd8k@ur\xb1MC'

def store_bookmark(url):
    bookmarks.append(dict(
        url = url,
        user = "reindert",
        date = datetime.utcnow()

    ))
def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

def find_similar_speaker(df, name):
    numerical = df.select_dtypes(include=['int64','float64'])
    df_normalized = (numerical - numerical.mean()) / numerical.std()
    df_normalized.drop(['conversation','music','index','languages','comments', 'duration', 'views','persuasive', 'unconvincing', 'inspiring', 'film_date', 'published_date','published_year','AllPunc','Period','Comma','Colon','SemiC','QMark','Exclam','Dash','Quote','Apostro','Parenth','OtherP', 'affect_1h','posemo_1h','negemo_1h', 'anx_1h', 'anger_1h', 'sad_1h', 'affect_2h', 'posemo_2h', 'negemo_2h', 'anx_2h', 'anger_2h', 'sad_2h', 'affect_1q', 'posemo_1q', 'negemo_1q', 'anx_1q', 'anger_1q', 'sad_1q', 'affect_2q', 'posemo_2q', 'negemo_2q', 'anx_2q', 'anger_2q', 'sad_2q', 'affect_3q', 'posemo_3q', 'negemo_3q', 'anx_3q', 'anger_3q', 'sad_3q', 'affect_4q', 'posemo_4q','negemo_4q', 'anx_4q', 'anger_4q','sad_4q','posemo_change_h', 'negemo_change_h','affect_change_h', 'posemo_change_q', 'negemo_change_q', 'affect_change_q'],axis=1,inplace=True)
    speaker_normalized = df_normalized[df["main_speaker"] == name]
    speaker_normalized = speaker_normalized.iloc[0]
    euclidean_distances = df_normalized.apply(lambda row: distance.euclidean(row, speaker_normalized), axis=1)
    second_smallest_value = euclidean_distances.nsmallest(2).iloc[1]
    rec_idx = euclidean_distances[euclidean_distances == second_smallest_value].index
    return df[['main_speaker', 'url' ]].iloc[rec_idx]



def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    df = read_data()
    name = request.form['text1']
    single_df = find_similar_speaker(df, name)
    data = single_df.to_html()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        url = request.form['url']
        store_bookmark(url)
        flash("Stored bookmark '{}'".format(url))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)


