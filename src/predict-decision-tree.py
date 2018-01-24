import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
import operator
import graphviz
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeRegressor


def read_data():
    df = pd.read_excel(os.path.join('..',settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

def sort_important_features(df):
    dt = DecisionTreeRegressor()
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    model = dt.fit(df[predictors], df[settings.TARGET])
    results = {name: score for name, score in zip(predictors, dt.feature_importances_)}
    sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    print("Feature Importances for the Response Variable: {}".format(settings.TARGET))
    for feat, importance in sorted_results:
        print("feature: {f}, importance: {i}".format(f=feat, i=importance))
    accuracy = dt.score(df[predictors], df[settings.TARGET])
    print("Accuracy: {}".format(accuracy))
    return model

def print_tree(model):
    # Where to save the figures
    PROJECT_ROOT_DIR = ".."
    IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images")
    path = os.path.join(IMAGES_PATH, "Decision Tree Predicting {}".format(settings.TARGET))
    predictors = df.columns.tolist()
    features = [p for p in predictors if p not in settings.NON_PREDICTORS]
    data = export_graphviz(model, out_file=None, feature_names=features)
    graph = graphviz.Source(data)
    graph.render(path, view=True)
    pass

if __name__ == "__main__":
    df = read_data()
    model = sort_important_features(df)
    print_tree(model)


