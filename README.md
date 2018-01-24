<a href="http://www.theodorespeaks.com"><img src="static/images/theodore-logo.png" height=70%  width=70%  alt="Insights from Persuasive TED Talks"></a>

[theodorespeaks.com](http://www.theodorespeaks.com)

[__Spring 2018 Galvanize Data Science Immersive__](https://www.galvanize.com/austin)

<br><br>
An Investigation of Persuasiveness using Natural Language Processing and Machine Learning.

__Abstract:__
A natural language processing project to reveal linguistic features that predict a persuasive TED Talk. I webscraped every TED Talk transcript and it's metadata from 2006 through 2017 and then used decision trees, random forest regressors, and linear regression to find key predictors of persuasive ratings by viewers. For professionals who need to communicate & influence others, TheodoreSpeaks.com is a data product to provide insights on how to speak to persuade.


__Results:__
I found that the change in negative and positive emotion words across the talk and the speaker’s use of key social pronouns like “I” and “we” made a big impact on persuasive ratings. My analyses resulted in a few important categories of words that make up a “linguistic signature” of persuasion and a classifier that you can use to predict the persuasiveness of your own text.



See this work as a presentation in [Google Slides](https://docs.google.com/presentation/d/1HuLg7flwSoy_YKFmS6S6ypa1kuKpDmKfMoaDjzYe5xc/edit?usp=sharing).

[See the video](https://youtu.be/6SmLwANBp_4) of this talk.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=6SmLwANBp_4" target="_blank"><img src="http://img.youtube.com/vi/6SmLwANBp_4/0.jpg" 
alt="Theodore Speaks - How to Persuade and Inspire Like TED" width="240" height="180" border="10" /></a>



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

The [TheodoreSpeaks web app](http://www.theodorespeaks.com) uses natural language processing techniques and the Linguistic Inquiry and Word Count (LIWC) module to analyze the transcripts of 2600+ TED Talks. The embedded models include decision trees, random forest regressors, and linear regression to find text categories with statistically significant relationships to TED.com user's ratings and to the number of times the talk has been viewed.

![how-it-works.png](https://media.data.world/xMzimqnhTnSgdNL8YcMe_how-it-works.png)

# Hypotheses

### General Hypothesis
A more persuasive, inspiring talk is related not just to WHAT people are saying but HOW they are saying it.

What people are saying:
- Content Words - job, brain, computer

How they are saying it:
- Emotion Words - happy, sad, angry
- Function Words - I, you, we, what


### Sub-Hypotheses

1. Emotion Words
 - Talks that use positive and negative emotion words in the shape of the Hero’s Journey will be more persuasive and inspiring.
2. Function Words
 - Socially powerful function words like "I, we, you" and "what, where, how" will be predictive of persuasive and inspiring ratings.
 
  - Talks that use “I, me, my” more will be less persuasive
  - Talks that use “we, us” more will be more inspiring



# Analysis methods

The tech stack consists of Python 3, Numpy, Pandas, Beautiful Soup, Linguistic Inquiry and Word Count (LIWC), Natural Language Toolkit (NLTK), Scikit-Learn, Matplotlib, HTML, CSS, Tableau, Flask, and Heroku.

Two ```csv``` files, the results of the webscraping, are stored in the ```data``` directory. 

```ted-main.csv``` has the metadata for 2638 TED Talks- all talks featured on TED.com from 2006 through 2017.
```transcripts.csv``` contains the transcripts for 2542 talks - the transcripts are not available for every talk.

Four text transcript files are also stored in the data directory. These transcripts cannot be stored in a CSV because they are larger than the 32,767 character limit for a cell.


To prepare the dataset for analyses:

From the ```src``` directory of the repo, run the following code:

```python assemble.py```

```python annotate.py```

```python process-text.py```

These scripts: 
- drop rows with missing transcripts
- remove talks centered around music performances
- remove talks with more than 1 speaker
- create features like 'applause', 'laughter' from transcript
- normalize ratings counts to account for number of times the talk has been viewed
- divide transcripts into quarters
- add results of LIWC analysis and create emotion word change features 

Edits to transcripts were done by script and by hand to remove question and answer sections and conversations with multiple speakers.

If structural changes to the cleaning and feature engineering are required, rerun the results of ```annotate.py```, the dataset in ```all_after_annotate.xls```, through LIWC module to produce per document word category ratios. A license with LIWC is required and is available at [liwc.net](http://www.liwc.net)</a>.

After running the 3 scripts above, you have a final dataset ```all_with_liwc_segmented.xls``` with features ready for statistical models (93.5 MB).




For all the following analyses, the response variable is set in the ```settings.py``` file, on line 3, under the variable name "TARGET".

For response variables, you might choose from 'norm_persuasive', 'norm_inspiring', 'views', 'comments', or 'applause'.

To fit a decision tree, and see the top feature importances, run:

```python predict-decision-tree.py```

To fit a random forest regressor and see the top feature importances, run:

```python predict-random-forest.py```

To build a linear regression model with most important features from the previous steps as predictors, run:

```python predict-linear.py```



To explore the 10 primary components in TED Talks using non-negative matrix factorization to perform clustering, run:

```python clustering.py``` 

To train a classifier model to predict 'persuasive' and 'non-persuasive' texts, run:

```python classification.py```

You can also access this classifier by visiting theodorespeaks.com, scrolling down, and inputting your own text into the text box and hitting "Submit".
The page will reload with a "Persuasive" or "Non-Persuasive" prediction with a probability beside the text box. 




# Results

#### Emotion Words Across All Talks

![image](https://www.filepicker.io/api/file/xDcgKi5GSW2AqhsTlBzQ)


#### Increased Persuasive Ratings
Text features that were associated with higher 'persuasive' ratings by TED.com users:

##### What You Say
- Risk
 - danger, doubt
- Moral
 - care, fair, loyal
- Money
 - audit, cash, owe

##### How You Say It
- Negative Emotion 
 - hurt, ugly, nasty
- Negate
 - no, not, never
- Question 
 - how, when, what
- Focus on Present 
 - today, is, now
- DECREASED “I” Words 
 - me, mine, I


![Screen Shot 2018-01-23 at 7.06.18 PM.png](https://media.data.world/si2aLadqTqOSl2I0gPah_Screen%20Shot%202018-01-23%20at%207.06.18%20PM.png)

Consistent with a Hero's Journey framework that calls for many challenges in the course of a narrative, increased use of negative emotion words like "sad, angry, depressed, frustrated" across all quarters of the talk was related to higher persuasive ratings by TED.com users.

![Screen Shot 2018-01-24 at 9.40.18 AM.png](https://media.data.world/MUjCqv3HTpuIKsmOrY28_Screen%20Shot%202018-01-24%20at%209.40.18%20AM.png)



#### Increased Inspiring Ratings

Text features that predicted higher 'inspiring' ratings by TED.com users:

##### What You Say
- Achievement 
 - win, success, better
- Power 
 - superior, bully

##### How You Say It
- Sad in 2nd Quarter 
 - crying, grief, sad
- Positive Emotion Change from Q1 to Q4
- We 
 - we, us, our
- “I” Words
 - me, mine, I

![image](https://www.filepicker.io/api/file/Q8pinlKTbe6FarVopj0c)

Consistent with a Hero's Journey storytelling framework, increased sad words in the 2nd quarter of talks were related to increased inspiring ratings.

![image](https://www.filepicker.io/api/file/oZbfeVcmSMasYRR8BDpd)



# Future improvements
- Further improve the accuracy of the online "submit a text" classifier model.
- Expand analyses to find the text features that predict more user comments online. 


# Acknowledgements

Thanks to Joseph Gartner, Dan Rupp, Andrew Kraemer, Andy Bashford, Tyler Watson, Michael Engeling, and Lee Harper for critical feedback and guidance during the development of this project.

Thanks also to [Reindert-Jan Ekker](https://app.pluralsight.com/library/courses/flask-micro-framework-introduction/table-of-contents) for an excellent introduction to the Flask microframework. 
Thanks also to [Rounak Banik](https://www.kaggle.com/rounakbanik) for a well organized open dataset that I used to supplement and verify the results of my webscraping.

# Web App

Visit [www.theodorespeaks.com](http://www.theodorespeaks.com) to see visualizations and tools built from these analyses.
 

