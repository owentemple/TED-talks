import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import settings
import pandas as pd
from scipy.stats import pearsonr


def read_data():
    df = pd.read_excel(os.path.join('..',settings.PROCESSED_DIR, "all_with_liwc_segmented.xls"), encoding="ISO-8859-1")
    return df

# Function outputs p-values of correlations in a similar format to pandas .corr function
def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues

# Create plot of words in 6 moral categories over time to see if increasing, decreasing, or flat
def plot_moral_words_by_year():
    df.groupby('published_year')['MoralityGeneral'].mean().plot()
    df.groupby('published_year')['Harm'].mean().plot()
    df.groupby('published_year')['Authority'].mean().plot()
    df.groupby('published_year')['Fairness'].mean().plot()
    df.groupby('published_year')['Ingroup'].mean().plot()
    df.groupby('published_year')['Purity'].mean().plot()

def correlation_and_pvalue_of_moral_words_over_time():
    # Create dataframe with only variables related to moral dimensions in talk transcripts
    moral_df = df[['MoralityGeneral', 'Harm', 'Authority', 'Ingroup', 'Purity', 'Fairness', 'published_date']]
    # Show correlation matrix of moral category by year to see if mentions of that dimension
    # are increasing, decreasing or flat over time
    print(moral_df.corr())
    # Show p-value of correlation of moral category by year. If output is 0 or below 0.05,
    # then p-value of correlation is significant
    print(calculate_pvalues(moral_df))



if __name__ == "__main__":
    df = read_data()
    plot_moral_words_by_year()
    correlation_and_pvalue_of_moral_words_over_time()