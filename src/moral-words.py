from scipy.stats import pearsonr

def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues

def plot_moral_words_by_year():
    df.groupby('published_year')['MoralityGeneral'].mean().plot()
    df.groupby('published_year')['Harm'].mean().plot()
    df.groupby('published_year')['Authority'].mean().plot()
    df.groupby('published_year')['Fairness'].mean().plot()
    df.groupby('published_year')['Ingroup'].mean().plot()
    df.groupby('published_year')['Purity'].mean().plot()

def correlation_and_pvalue_of_moral_words_over_time():
    # Show correlation matrix of moral category by year
    df[['MoralityGeneral', 'Harm', 'Authority', 'Ingroup', 'Purity', 'Fairness', 'published_date']].corr()
    # Show p-value of correlation of moral category by year
    moral_df = df[['MoralityGeneral', 'Harm', 'Authority', 'Ingroup', 'Purity', 'Fairness', 'published_date']]
    calculate_pvalues(moral_df)





if __name__ == "__main__":