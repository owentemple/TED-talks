from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
import os
import settings
import pandas as pd
import numpy as np
import pickle
from scipy.spatial import distance
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from nltk.stem.snowball import SnowballStemmer

app = Flask(__name__)

bookmarks = []
app.config['SECRET_KEY'] = '+\xb3N\xc0\xe90A\x8d1Lv\x87\x13\xf8\xecY\xd8k@ur\xb1MC'

stemmer = SnowballStemmer('english')


class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

def store_bookmark(url):
    bookmarks.append(dict(
        url = url,
        user = "TEDster",
        date = datetime.utcnow()
    ))

def read_data():
    df = pd.read_excel(os.path.join(settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

def find_similar_speaker(df, name):
    numerical = df.select_dtypes(include=['int64','float64'])
    df_normalized = (numerical - numerical.mean()) / numerical.std()
    df_normalized.drop(['conversation','music','index','languages','comments', 'duration', 'views','persuasive', 'unconvincing', 'inspiring', 'film_date', 'published_date','published_year','AllPunc','Period','Comma','Colon','SemiC','QMark','Exclam','Dash','Quote','Apostro','Parenth','OtherP', 'affect_1h','posemo_1h','negemo_1h', 'anx_1h', 'anger_1h', 'sad_1h', 'affect_2h', 'posemo_2h', 'negemo_2h', 'anx_2h', 'anger_2h', 'sad_2h', 'affect_1q', 'posemo_1q', 'negemo_1q', 'anx_1q', 'anger_1q', 'sad_1q', 'affect_2q', 'posemo_2q', 'negemo_2q', 'anx_2q', 'anger_2q', 'sad_2q', 'affect_3q', 'posemo_3q', 'negemo_3q', 'anx_3q', 'anger_3q', 'sad_3q', 'affect_4q', 'posemo_4q','negemo_4q', 'anx_4q', 'anger_4q','sad_4q','posemo_change_h', 'negemo_change_h','affect_change_h', 'posemo_change_q', 'negemo_change_q', 'affect_change_q','HarmVirtue', 'HarmVice', 'AuthorityVirtue','AuthorityVice','FairnessVirtue','FairnessVice','IngroupVirtue', 'IngroupVice', 'PurityVirtue', 'PurityVice', 'Moral', 'MoralityGeneral'],axis=1,inplace=True)
    speaker_normalized = df_normalized[df["main_speaker"] == name]
    speaker_normalized = speaker_normalized.iloc[0]
    euclidean_distances = df_normalized.apply(lambda row: distance.euclidean(row, speaker_normalized), axis=1)
    second_smallest_value = euclidean_distances.nsmallest(2).iloc[1]
    rec_idx = euclidean_distances[euclidean_distances == second_smallest_value].index
    return df[['main_speaker', 'description','url' ]].iloc[rec_idx]

# The fit classifier is only run manually when updating classifier model
def fit_classifier(df):
    persuasive_median = df['norm_persuasive'].median()
    df['persuasive_label'] = np.where(df['persuasive'] >= persuasive_median, 1, 0)
    count_vect = StemmedCountVectorizer(analyzer="word", stop_words='english', min_df=2)
    X_train_counts = count_vect.fit_transform(df['transcript'])
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, df['persuasive_label'])
    return clf, count_vect, tfidf_transformer

def dump_model(clf, count_vect, tfidf_transformer):
    # Dump the trained multinomial classifier with Pickle
    multinomial_pkl_filename = 'multinomial_classifier_20180117.pkl'
    # Open the file to save as pkl file
    multinomial_model_pkl = open(multinomial_pkl_filename, 'wb')
    pickle.dump(clf, multinomial_model_pkl)
    # Close the pickle instances
    multinomial_model_pkl.close()

    # Dump the trained vectorizer with Pickle
    vectorizer_pkl_filename = 'vectorizer_20180117.pkl'
    # Open the file to save as pkl file
    vectorizer_model_pkl = open(vectorizer_pkl_filename, 'wb')
    pickle.dump(count_vect, vectorizer_model_pkl)
    # Close the pickle instances
    vectorizer_model_pkl.close()

    # Dump the trained tfidf with Pickle
    tfidf_pkl_filename = 'tfidf_20180117.pkl'
    # Open the file to save as pkl file
    tfidf_model_pkl = open(tfidf_pkl_filename, 'wb')
    pickle.dump(tfidf_transformer, tfidf_model_pkl)
    # Close the pickle instances
    tfidf_model_pkl.close()
    pass

def load_model():
    my_dir = os.path.dirname(__file__)
    multinomial_pkl_filename = 'multinomial_classifier_20180117.pkl'
    vectorizer_pkl_filename = 'vectorizer_20180117.pkl'
    tfidf_pkl_filename = 'tfidf_20180117.pkl'
    # Loading the saved multinomial model pickle
    multinomial_model_pkl = open(os.path.join(my_dir, multinomial_pkl_filename), 'rb')
    clf = pickle.load(multinomial_model_pkl)
    print("Loaded Multinomial model :: ", clf)

    # Loading the saved vectorizer model pickle
    vectorizer_model_pkl = open(os.path.join(my_dir,vectorizer_pkl_filename), 'rb')
    count_vect = pickle.load(vectorizer_model_pkl)
    print("Loaded Vectorizer model :: ", count_vect)

    # Loading the saved tfidf model pickle
    tfidf_model_pkl = open(os.path.join(my_dir,tfidf_pkl_filename), 'rb')
    tfidf_transformer = pickle.load(tfidf_model_pkl)
    print("Loaded TFIDF model :: ", tfidf_transformer)
    return clf, count_vect, tfidf_transformer


def predict_new(clf, count_vect, tfidf_transformer, speech):
    new_counts = count_vect.transform([speech])
    X_new_tfidf = tfidf_transformer.transform(new_counts)
    prediction = clf.predict(X_new_tfidf)
    probability = clf.predict_proba(X_new_tfidf)

    return prediction[0], probability[0][1]


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
    result = single_df.to_dict()
    data = []
    for k,v in result.items():
        for key, value in v.items():
            data.append(value)
    speaker_name = data[0]
    description = data[1]
    url_rx = data[2]

    return render_template('index.html', speaker_name=speaker_name, description=description, url_rx=url_rx)

@app.route('/predict_text', methods=['POST'])
def predict_text():
    speech = request.form['text2']
    clf, count_vect, tfidf_transformer = load_model()
    result = predict_new(clf, count_vect, tfidf_transformer, speech)
    message = "PERSUASIVE - " if result[0] == 1 else "NOT PERSUASIVE - "
    percentage = str(round(result[1] * 100,2)) + "% Probability of Persuasive Rating"
    return render_template('index.html', message=message, percentage=percentage)

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

#when need to fit and dump a new model, uncomment 3 lines below and run ```python theodore.py```
#df = read_data()
#clf, count_vect, tfidf_transformer = fit_classifier(df)
#dump_model(clf, count_vect, tfidf_transformer)

if __name__ == "__main__":
    # multinomial_pkl_filename = 'multinomial_classifier_20180117.pkl'
    # vectorizer_pkl_filename = 'vectorizer_20180117.pkl'
    # tfidf_pkl_filename = 'tfidf_20180117.pkl'
    # clf, count_vect, tfidf_transformer = load_model()
    app.run(debug=True)







