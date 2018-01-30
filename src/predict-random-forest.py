import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

# Read in the data
def read_data():
    df = pd.read_excel(os.path.join('..', settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

# Fit random forest regressor and store feature importances and column names in a dictionary
# Print sorted feature importances descending by magnitude
def sort_important_features(df):
    rf = RandomForestRegressor()
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    model = rf.fit(df[predictors], df[settings.TARGET])
    importances = rf.feature_importances_

    results = {name: score for name, score in zip(predictors, importances)}
    print("Feature Importances for the Response Variable: {}".format(settings.TARGET))
    sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    for feat, importance in sorted_results:
        print('feature: {f}, importance: {i}'.format(f=feat, i=importance))
    accuracy = rf.score(df[predictors], df[settings.TARGET])
    print("Accuracy: {}".format(accuracy))
    names = [k[0] for k in sorted_results]
    return model, importances, names

# Create horizontal bar chart showing feature importances descending by magnitude
def plot_feature_importances(df, importances, names):
    reversed_names = names[::-1]
    predictors = df.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    features = predictors
    indices = np.argsort(importances)

    plt.figure(figsize=(30, 60))
    matplotlib.rcParams.update({'font.size': 22})
    plt.title('Feature Importances Predicting {}'.format(settings.TARGET))
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), reversed_names)
    plt.xlabel('Relative Importance')
    save_fig('Feature Importances Predicting {}'.format(settings.TARGET))
    pass

# Save the figure of feature importances in the 'images' folder
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    # Where to save the figures
    PROJECT_ROOT_DIR = ".."
    IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images")
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    pass


if __name__ == "__main__":
    df = read_data()
    rf, importances, names = sort_important_features(df)
    plot_feature_importances(df, importances, names)
