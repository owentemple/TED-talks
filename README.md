<a href="http://www.theodorespeaks.com"><img src="static/images/theodore-logo.png" height=70%  width=70%  alt="Insights from Persuasive TED Talks"></a>

[theodorespeaks.com](http://www.theodorespeaks.com)

[__Spring 2018 Galvanize Data Science Immersive__](https://www.galvanize.com/austin)

<br><br>
An Investigation of Persuasiveness using Natural Language Processing and Machine Learning.

__Abstract:__
A natural language processing project to reveal linguistic features that predict a persuasive TED Talk. I webscraped every TED Talk transcript and it's metadata from 2006 through 2017 and then used decision trees, random forest regressors, and linear regression to find key predictors of persuasive ratings by viewers. For professionals who need to communicate & influence others, TheodoreSpeaks.com is a data product to provide insights on how to speak to persuade.


__Results:__
I found that the change in negative and positive emotion words across the talk and the speaker’s use of key social pronouns like “I” and “we” made a big impact on persuasive ratings. My analyses resulted in a few important categories of words that make up a “linguistic signature” of persuasion and a classifier that you can use to predict the persuasiveness of your own text.

Increased use of the

See this work as a presentation in [Google Slides](https://docs.google.com/presentation/d/1HuLg7flwSoy_YKFmS6S6ypa1kuKpDmKfMoaDjzYe5xc/edit?usp=sharing).

[See the video](https://youtu.be/6SmLwANBp_4) of this talk.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=6SmLwANBp_4" target="_blank"><img src="http://img.youtube.com/vi/6SmLwANBp_4/0.jpg" 
alt="Theodore Speaks - Lightning Talk" width="240" height="180" border="10" /></a>

<br clear="right">

# Background & Motivation
Whether or not you ever give a TED Talk yourself, and no matter what your job title is - developer, data scientist, or recruiter - your job is ultimately to communicate and influence, so the words you say matter. Whether it's a morning stand up meeting, a training, or a conference call, you need to persuade and, sometimes, even inspire.

What better way to learn how to persuade and inspire than from the masters of persuasion - TED speakers?

I’m a TED Talks enthusiast - I’ve watched one a day for 3 years - and I noticed that some talks are persuasive— they change your day and maybe your life. Some others, fall flat and are completely forgettable.

Can we use the tools of natural language processing and statistical models to understand why some talks work - to see how persuaders persuade?


## The Problem
Your job, no matter the title, is to influence and persuade others. 

Can we use successful TED Talks to learn how to become more persuasive communicators?

## The Solution

For professionals who need to understand how to persuade and inspire, my product is takes data from TED.com uses natural language processing techniques and runs text through a series of data science models to provide insights on HOW to speak to be persuasive.	The product is called TheodoreSpeaks.com.


# Analysis methods

The tech stack consists of Python 3, Numpy, Pandas, Beautiful Soup, Linguistic Inquiry and Word Count (LIWC), Natural Language Toolkit (NLTK), Scikit-Learn, Matplotlib, HTML, CSS, Tableau, Flask, and Heroku.

Two csvs, the results of the webscraping, are stored in the data directory. 

```ted-main.csv``` has the metadata for 2638 TED Talks- all talks featured on TED.com from 2006 through 2017.
```transcripts.csv``` contains the transcripts for 2542 talks - the transcripts are not available for every talk.

Four text transcript files are also stored in the data directory. These transcripts cannot be stored in a CSV because they are larger than the 32,767 character limit for a cell.


To prepare the dataset for analyses:

From the ```src``` directory of the repo, run the following code:

```python assemble.py```

```python annotate.py```

```python process-text.py```

Now you have a dataset with features ready for statistical models.


I fit decision trees, random forest regressors, and linear regression to find the important text features that were associated with higher 'persuasive' ratings by TED.com users.

- Risk Words - danger, doubt
- Negate Words - no, not, never
- Moral Words - care, fair, loyal
- Money - audit, cash, owe
- Quantifiers - few, many, much
- Negative Emotion - hurt, ugly, nasty
- Question Words - how, when, what
- Focus Present - today, is, now
- Decreased "I" Word Usage  - I, me, mine

![Screen Shot 2018-01-17 at 2.47.13 PM.png](https://media.data.world/zYJz6G60RtWLrDcCRvfM_Screen%20Shot%202018-01-17%20at%202.47.13%20PM.png)


For all the following analyses, the response variable is set in the ```settings.py``` file, on line 3, under the variable name "TARGET".

You can choose from 'norm_persuasive', 'norm_inspiring', 'views', 'comments', or 'applause'.

To fit a decision tree, and see the top feature importances, run:

```python predict-decision-tree.py```

To fit a random forest regressor and see the top feature importances, run:

```python predict-random-forest.py```

To build a linear regression with most important features from the previous steps, run:

```python predict-linear.py```


# Future improvements



# Acknowledgements


# References :
