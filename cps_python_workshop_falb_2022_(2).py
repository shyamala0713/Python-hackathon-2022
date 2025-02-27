# -*- coding: utf-8 -*-
"""CPS_Python_Workshop_FalB_2022 (2).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1seb7pPwGmhDsK3br7CW0dWfGacrv-fop

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/en/thumb/b/bd/Northeastern_University_seal.svg/225px-Northeastern_University_seal.svg.png">
</p>
<h2><center>College of Professional Studies</center></h2>
<h2><center>Northeastern University Silicon Valley</center></h2>
<h3><center>CPS Python Workshop</center></h3>
<h3><center>Hackthon: Thematic Analysis of Song Lyrics</center></h3>
<h3><center>Submitted on:</center></h3> 
<font size="4"><center>Nov 23, 2022</center></font>
<h3><center>Submitted to:</center></h3>
<font size="4"><center>Professor: Dr. Shanu Sushmita</center></font>
<font size="4"><center>Dr. Ghazal Tariri</center></font>
<font size="4"><center>Mohammad Zandsalimy</center></font>
<h3><center>Submitted by:</center></h3>
<font size="4"><center>Nikshita Ranganathan</center></font>
<font size="4"><center>Pavan Kumar Bansal</center></font>
<font size="4"><center>Shyamala Venkatakrishnan</center></font>

## Table of Contents:

> <font size="4">1. [Introduction](#introduction)</font>

> <font size="4">2. [Analysis](#Analysis)</font>
  
> <font size="4">3. [Conclusion](#Conclusion)</font>

> <font size="4">4. [References](#References)</font>

> <font size="4">5. [Appendix](#Appendix)</font>

<h2><center>Introduction <a name="introduction"></a></center></h2>

We have used the Song Lyrics dataset fro Kaggle site, which has several artist's data over varity of genres.
We are going to use the Google Colob to run this code becuase of the volume of file using the GPU.

Below is our pipeline approach for this project:

**Data cleaning :**
  -  Rename
  -  Removing NA
  -  Filling missing values

**EDA :**
  - Top  songs in each genre based on popularity 
  - Artist with most songs
  - Artist with most popularity
  - Most popular genre

**NLP :**
  - Lowercasing
  - tokenization
  - stopwords
  - punctuation removal
  - Frequency Distribution , Condition frequecny Distribution
  - Sentiment/emotion
  - Reletive frequecny
  - Word cloud using word Net

<h2><center>Analysis <a name="Analysis"></a></center></h2>

# Setting up the environment
"""

from google.colab import drive
drive.mount('/content/drive')

import nltk
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#Tokenization of text
from nltk.tokenize import word_tokenize,sent_tokenize
#remove stop-words
from nltk.corpus import stopwords # library 
nltk.download('stopwords')
from nltk.stem import PorterStemmer
all_stopwords = set(stopwords.words('english')) # set the language 
from typing import List
nltk.download('punkt')
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator

# please for code here
lyrics = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Hackthondata.csv')
lyrics.info()

lyrics.head(5)

"""**Renaming the columns**"""

lyrics.columns = ['Song_name', 'Song_Link', 'Lyrics', 'Language','Artist','Genre','Songs','Popularity','Artist_link']
lyrics = lyrics.drop(columns=['Song_Link', 'Artist_link', 'Language'])

"""**Dropping the unwanted columns**"""

lyrics.head(10)

"""**Visualization and Removal of NA values**





"""

lyrics.isnull().sum()

plt.figure(figsize=(10,6))
sns.displot(
    data=lyrics.isna().melt(value_name="missing"),
    y="variable",
    hue="missing",
    multiple="fill",
    aspect=1.25
)
plt.savefig("visualizing_missing_data_with_barplot_Seaborn_distplot.png", dpi=100)

plt.figure(figsize=(10,6))
sns.heatmap(lyrics.isna().transpose(),
            cmap="YlGnBu",
            cbar_kws={'label': 'Missing Data'})
plt.savefig("visualizing_missing_data_with_heatmap_Seaborn_Python.png", dpi=100)

cleanlyrics=lyrics.dropna()

cleanlyrics.isnull().sum()

cleanlyrics['Genre'].to_string()

song_df = cleanlyrics.copy(deep=True)

song_df['Genre'] = song_df['Genre'].apply(lambda x:str(x).split(";")[0])

song_df['Genre'].unique()

"""# Analyzing the dataset : EDA"""

cleanlyrics

cleanlyrics.info()

cleanlyrics.dtypes

cleanlyrics.shape

cleanlyrics.describe()

cleanlyrics['Number_of_words'] = cleanlyrics['Lyrics'].apply(lambda x:len(str(x).split()))

plt.style.use('ggplot')
plt.figure(figsize=(12,6))
sns.distplot(cleanlyrics['Number_of_words'],kde = False,color="coral",bins=200)
plt.title("Frequency distribution of number of words for each song", size=20)
plt.xlim(0,1000)
plt.xlabel("Number of words")
plt.ylabel("Count")

plt.hist(cleanlyrics['Popularity'],color="skyblue")
plt.title("Distribution of popularity score of songs", size=20)
plt.xlabel("Song popularity")
plt.ylabel("Count")
plt.xlim(0,100)

song_df['Genre'].unique()

!pip install sqldf
import sqldf as sql

query = """
SELECT Genre,avg(Popularity) as popularity_score
FROM song_df
group by Genre
order by popularity_score desc limit 10;
"""

popular_genre_df= sql.run(query)

popular_genre_df

plt.figure(figsize=(14, 8))
plt.barh(popular_genre_df['Genre'], popular_genre_df['popularity_score'], color = 'maroon')
plt.xlabel("Average popularity score of songs")
plt.ylabel("Genres")
plt.title("Top 10 genres with songs having highest average popularity score")
plt.show()

query = """
SELECT Artist,count(Song_name) as Total_songs
FROM song_df
group by Artist 
order by Total_songs desc limit 20;
"""

artist_songs_df= sql.run(query)

artist_songs_df

plt.figure(figsize=(14, 8))
plt.hlines(y=artist_songs_df['Artist'], xmin=0, xmax=artist_songs_df['Total_songs'], color='skyblue')
plt.plot(artist_songs_df['Total_songs'], artist_songs_df['Artist'], "D")
plt.xlabel("No. of songs")
plt.ylabel("Artist")
plt.title("Top 20 artists with the most number of songs")
plt.show()

query = """
SELECT Artist,avg(Popularity) as popularity_score
FROM song_df
group by Artist
order by popularity_score desc limit 10;
"""

popular_artist_df= sql.run(query)

popular_artist_df

plt.figure(figsize=(14, 8))

sns.barplot(x="Artist", y="popularity_score", data=popular_artist_df, estimator=np.mean, ci=95, capsize=.2, color='green')
plt.xlabel("Artist")
plt.ylabel("Average popularity score of songs")
plt.title("Top 10 artists with most popular songs")

query = """
SELECT Song_name,Popularity,Genre, Lyrics
FROM song_df
where Genre = 'Trip-Hop'
order by Popularity desc limit 5;
"""
popular_songs_df1= sql.run(query)
popular_songs_df1

query = """
SELECT Song_name,Popularity,Genre,Lyrics
FROM song_df
where Genre = 'Hard Rock'
order by Popularity desc limit 5;
"""
popular_songs_df2= sql.run(query)
popular_songs_df2

query = """
SELECT Song_name,Popularity,Genre,Lyrics
FROM song_df
where Genre = 'Pop'
order by Popularity desc limit 5;
"""
popular_songs_df3= sql.run(query)
popular_songs_df3

query = """
SELECT Song_name,Popularity,Genre,Lyrics
FROM song_df
where Genre = 'Surf Music'
order by Popularity desc limit 5;
"""
popular_songs_df4= sql.run(query)
popular_songs_df4

query = """
SELECT Song_name,Popularity,Genre,Lyrics
FROM song_df
where Genre = 'Rockabilly'
order by Popularity desc limit 5;
"""
popular_songs_df5= sql.run(query)
popular_songs_df5

popular_songs_df1 = popular_songs_df1.append(popular_songs_df2).append(popular_songs_df3).append(popular_songs_df4).append(popular_songs_df5)

popular_songs_df1

import plotly.express as px
plt.figure(figsize=(20, 12))  
fig = px.sunburst(popular_songs_df1, path=['Genre', 'Song_name'], 
                  values='Popularity',title='Genre wise top 5 popular songs')
fig

"""# NLP , word analysis 
## keywords:
  - love
  - like
  - hate
  - dance
  - friend
  - good
  - bad
  - people
  - feel
  - baby
"""

keywords= ['love','like','hate','dance','friend','good','bad','people','feel','baby']

def remove_delimiters(sentence):
    return re.sub(r'[^\w\s]', '', sentence)

def tokenization(lyrics):
    lowercase_word_corpus=[]
    trimmed_sentences=remove_delimiters(lyrics)
    word_corpus = word_tokenize( trimmed_sentences)   
    ps = PorterStemmer()
    filtered_words = [ps.stem(w) for w in word_corpus]
    lowercase_word_corpus = [re.sub(r'\W+', '', word.lower()) for word in word_corpus] 
    return lowercase_word_corpus


def top_words(words,inputlist):
    lowercase_word_corpus=tokenization(words)
    if inputlist!="":
      fdist=nltk.FreqDist((word) for word in lowercase_word_corpus if word in inputlist)
    else :
      fdist=nltk.FreqDist((word) for word in lowercase_word_corpus)
    total_models=sum(fdist.values())
    for modelfreq in fdist.keys():
      fdist[modelfreq] /= total_models
    df=pd.DataFrame(list(fdist.items()), columns = ["Keyword","Reletive frequency"])
    df.set_index("Keyword", inplace=True) 
    return df


def wordcloud_out(word_corpus, title):
  wordcloud = WordCloud(stopwords=all_stopwords, colormap='tab20c').generate(word_corpus)
  plt.figure( figsize=(10,8))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.title(title, fontsize=13)
  plt.axis("off")
  plt.show()

"""#### Top songs analysis"""

All_Lyrics=[]
All_Lyrics.extend(popular_songs_df1['Lyrics'])
All_Lyrics=''.join(map(str,All_Lyrics))

freq_distribtuion = top_words(All_Lyrics,keywords) 
freq_distribtuion
sns.heatmap(freq_distribtuion, cmap ='RdYlGn', linewidths = 0.50, annot = True)

wordcloud_out(All_Lyrics, "Top Keywords")

"""# Popular Artist word choices"""

Popular_Artists= popular_artist_df["Artist"]
def artist_fev(artists):
  artist_Lyrics_dict={}
  for artist in artists:
       artist_Lyrics=[]   
       artist_Lyrics.extend( song_df.loc[song_df['Artist'] == artist] ['Lyrics'])
       artist_Lyrics=''.join(map(str,artist_Lyrics))
       artist_Lyrics_dict[artist]=artist_Lyrics
  return artist_Lyrics_dict

Popular_Artist_Lyrics_dict=artist_fev(Popular_Artists)
Popular_Artist_Lyrics=pd.DataFrame.from_dict(Popular_Artist_Lyrics_dict, orient ='index')
Popular_Artist_Lyrics

for artist in Popular_Artists:
       wordcloud_out(Popular_Artist_Lyrics.loc[artist][0], "Keywords used by"+":" + artist)

cfd= nltk.ConditionalFreqDist((Artist, word.lower()) for Artist in Popular_Artists 
                              for word in tokenization(Popular_Artist_Lyrics_dict[Artist]) if word.lower() in keywords)

relative_frequenency_distribtuion=pd.DataFrame(cfd)
relative_frequenency_distribtuion=(relative_frequenency_distribtuion/relative_frequenency_distribtuion.sum())
relative_frequenency_distribtuion
relative_frequenency_distribtuion.style.background_gradient(axis=0)

"""# Popular Genres """

top_genres= popular_genre_df["Genre"]
def genre_fev(genres):
  Top_genre_Lyrics_dict={}
  for genre in genres:
       Top_genre_Lyrics=[]   
       Top_genre_Lyrics.extend( song_df.loc[song_df['Genre'] == genre] ['Lyrics'])
       Top_genre_Lyrics=''.join(map(str,Top_genre_Lyrics))
       Top_genre_Lyrics_dict[genre]=Top_genre_Lyrics
  return Top_genre_Lyrics_dict
Top_genre_Lyrics_dict=genre_fev(top_genres)
Top_genre_Lyrics=pd.DataFrame.from_dict(Top_genre_Lyrics_dict, orient ='index')
Top_genre_Lyrics

for genre in top_genres:
       wordcloud_out(Top_genre_Lyrics.loc[genre][0], "Keywords used in"+":" + genre)

cfd= nltk.ConditionalFreqDist((genre, word.lower()) for genre in  top_genres
                              for word in tokenization(Top_genre_Lyrics_dict[genre]) if word.lower() in keywords)

relative_frequenency_distribtuion=pd.DataFrame(cfd)
relative_frequenency_distribtuion.style.background_gradient(axis=0)

"""# Sentiment analysis for Top Artists"""

# This piece of code is refered from the Keggle  
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def setimentanalyzer(df):
    neg='Negative'
    neu='Neutral'
    pos='Positive'
    negative = []
    neutral = []
    positive = []
    dominant_sentiment=[]
    dominant_sentiment_score=[]
    #Initialize the model
    sid = SentimentIntensityAnalyzer()
    #Iterate for each row of lyrics and append the scores
    for i in df.index:       
        scores = sid.polarity_scores(df.loc[i][0])
        negative.append(scores['neg'])
        neutral.append(scores['neu'])
        positive.append(scores['pos'])
        if scores['neg']>scores['pos']:
            dominant_sentiment_score.append(scores['neg'])
            dominant_sentiment.append(neg)
        elif scores['neg']<scores['pos']:
            dominant_sentiment_score.append(scores['pos'])
            dominant_sentiment.append(pos)
        else:
            dominant_sentiment_score.append(scores['neu'])
            dominant_sentiment.append(neu)
    #Create 5 columns to the main data frame  for each score
    df['negative'] = negative
    df['neutral'] = neutral
    df['positive'] = positive
    df['dominant_sentiment']=dominant_sentiment
    df['dominant_sentiment_score']=dominant_sentiment_score
    return df

setimentanalyzer(Popular_Artist_Lyrics)

sentiment= setimentanalyzer(Popular_Artist_Lyrics).drop(0, axis=1)

sentiment.style.background_gradient(axis=0)

"""<h2><center>Conclusion <a name="Conclusion"></a></center></h2> 

The above analysis is a clear walkthrough of NLP tasks, and it was great learning to understand the concept of text tokenization, normalization, and analyzing the reason behind some words’ repetition in the text, and can interpret the context of the text. For someone like me who is learning ML and NLP from the basics, it was a good exercise.

In the end, We would say thanks to the professor again to deliver such a wonderful session and provide us with an opportunity to learn python  from the basics. 

</br>
</br>
</br>

<h2><center>References: <a name="References"></a></center></h2> 

[1] Accessing Text Corpora and Lexical Resources. (n.d.). https://www.nltk.org/book/ch02.html 

[2] GeeksforGeeks. (2018, December 18). Get the index of minimum value in DataFrame column. https://www.geeksforgeeks.org/get-the-index-of-minimum-value-in-dataframe-column/ 

[3] Gübür, K. T. (2022, April 20). NLTK and Python WordNet: Find Synonyms and Antonyms with Python. Holistic SEO. https://www.holisticseo.digital/python-seo/nltk/wordnet 

[4] How to set Column as Index in Pandas DataFrame? - Python Examples. (n.d.). https://pythonexamples.org/pandas-set-column-as-index/ 

[5] nltk.ConditionalFreqDist. (n.d.). https://tedboy.github.io/nlps/generated/generated/nltk.ConditionalFreqDist.html 

[6] pandas.DataFrame.from_dict — pandas 1.5.1 documentation. (n.d.). https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.from_dict.html 

[7] Post author: Malli. (2022, January 6). Spark by {Examples}. https://sparkbyexamples.com/pandas/pandas-get-total-of-column/ 

[8] Python: Get Dictionary Key with the Max Value (4 Ways). (2022, February 23). Datagy. https://datagy.io/python-get-dictionary-key-with-max-value/ 

[9] Song Lyrics Dataset. (2021, February 8). Kaggle. https://www.kaggle.com/datasets/deepshah16/song-lyrics-dataset/code  

</br>
</br>
</br>

<h2><center>Appendix: <a name="Appendix"></a></center></h2>

Below HTML code we used for shaping the document by applying some CSS styling.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%html
# <style>
# .rendered_html {
#     font-size: 16px;
#     font-family: Times New Roman, serif;
#     line-height: 2;
#     text-align:left;
# }
# </style>