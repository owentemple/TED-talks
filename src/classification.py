import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.feature_extraction import text

stemmer = SnowballStemmer('english')

# Custom class that adds stemmer to sklearn's CountVectorizer
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])


def read_data():
    df = pd.read_excel(os.path.join('..',settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

# For classifier, create "persuasive" = 1 and "non-persuasive" = 0 labels from median split
def create_variables_with_median_split():
    persuasive_median = df['norm_persuasive'].median()
    df['persuasive_label'] = np.where(df['persuasive'] >= persuasive_median, 1, 0)
    pass

# Vectorize with stemmer, TF-IDF, test-split data, fit Multinomial Bayes
def fit_classifier():
    my_additional_stop_words = ['__']
    stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)
    count_vect = StemmedCountVectorizer(analyzer="word", stop_words='english', min_df=2)
    X_train_counts = count_vect.fit_transform(df['transcript'])
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print(X_train_tfidf.shape)

    X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, df['persuasive_label'])
    clf = MultinomialNB().fit(X_train, y_train)
    predicted = clf.predict(X_test)
    print("Accuracy of the classifier model is: {}%".format(clf.score(X_test, y_test)))

    # calculate null accuracy in a single line of code
    # only for binary classification problems coded as 0/1
    null_accuracy = max(y_test.mean(), 1 - y_test.mean())
    print("Null accuracy is: {}".format(null_accuracy))

    # Create confusion matrix to see misclassified rows
    standard_confusion_matrix(y_test, predicted)

    # Calculate recall and print result
    recall = recall_score(y_test, predicted)
    print("Recall is: {}".format(recall))

    #Calculate precision and print result
    precision = precision_score(y_test, predicted)
    print("Precision is: {}".format(precision))

    #Calculate F1 and print result
    F1 = 2 * (precision * recall) / (precision + recall)
    print("F1 score is: {}".format(F1))
    return count_vect, tfidf_transformer, clf


def standard_confusion_matrix(y_true, y_pred):
    """Make confusion matrix with format:
                  -----------
                  | TP | FP |
                  -----------
                  | FN | TN |
                  -----------
    Parameters
    ----------
    y_true : ndarray - 1D
    y_pred : ndarray - 1D

    Returns
    -------
    ndarray - 2D
    """
    [[tn, fp], [fn, tp]] = confusion_matrix(y_true, y_pred)
    return np.array([[tp, fp], [fn, tn]])

# Print the most informative features that classifier uses to distinguish 'persuasive' from 'not persuasive' talks
def show_most_informative_features(vectorizer, clf, n=50):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    top_words = []
    print("Most Informative Features ('Non-Persuasive' in the left column, 'Persuasive' on the right)")
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        top_words.append((coef_2, fn_2))
        print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))
    top_words_df = pd.DataFrame(top_words, columns=['coefficient', 'word'])
    # To produce csv output of this function, uncomment the following line
    #top_words_df.to_csv('top-words-persuasive.csv')
    return top_words_df


if __name__ == "__main__":
    df = read_data()
    create_variables_with_median_split()
    count_vect, tfidf_transformer, clf = fit_classifier()
    top_words_df = show_most_informative_features(count_vect, clf)