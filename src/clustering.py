import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import Stemmer

english_stemmer = Stemmer.Stemmer('en')


def read_data():
    df = pd.read_excel(os.path.join('..',settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

# custom class using sklearn's TfidfVectorizer to add stemmer
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: english_stemmer.stemWords(analyzer(doc))

# prints
def words_and_topics(h, words):
    top10 = np.flip(h.argsort(axis=1), axis=1)[:, :10]
    topics_list= []
    for topic in top10:
        print(words[topic])
        topics_list.append(words[topic])
    pass

# Vectorizes, stems, and TFIDF transforms passed in content
# Fits a non-negative matrix factorization model for specified number of components
# Prints components as lists
def fit_NMF(content, n_components):
    vect = StemmedTfidfVectorizer(min_df=2, stop_words='english', analyzer='word', ngram_range=(1,1))
    X = vect.fit_transform(content)
    column_names = np.array(vect.get_feature_names())
    model = NMF(n_components=n_components, max_iter=100)
    model.fit(X)
    w_sk = model.transform(X)
    h_sk= model.components_
    print("The {} Components in The Text Content:".format(n_components))
    print(words_and_topics(h_sk, column_names))
    pass


if __name__ == "__main__":
    df = read_data()
    # uses all TED Talks as content
    content = df['transcript'].as_matrix()
    # Finds the 10 components in all TED Talks
    fit_NMF(content, 10)