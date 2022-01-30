# -*- coding: utf-8 -*-
"""twitter-sentiment-analysis-SPAIN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kSayF7bufyjjKlmkjWBzSQePZubsUFBs
"""

import tweepy
import pandas as pd
from textblob import TextBlob 
import re 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
nltk.download("popular")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentiment_analysis_spanish import sentiment_analysis


##SENTIMENT ANALYSIS

def clean_tweet_text(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

!pip install googletrans==3.1.0a0
from googletrans import Translator, constants

def get_tweet_sentiment(tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(translator.translate(clean_tweet_text(tweet), dest="en").text) 
        # sentiment.sentiment(clean_tweet_text(tweet))
        
        # set sentiment
        # if(analysis.detect_language()== 'es'):
        # analysis= analysis.translate(from_lang='es',to='en') 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
          return 'neutral'
        else:
          return 'negative'

if __name__ == "__main__": 
    translator = Translator()
    #cargamos los datos del csv a fetched_tweets
    #fetched_tweets = pd.read_csv("_________.csv", header=0, usecols=['Text'])
    fetched_tweets = pd.read_csv("tweetsESPfil.csv", ',')
    fetched_tweets.text = fetched_tweets.text.apply(
    lambda x:x[2:-1].encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
)
    # print(fetched_tweets)
    count=0
    try:
        # relacionando text con sentiment 
        sentiment_sum = {'text': [], 'sentiment': []}  

        #iteramos la columna para extraer el sentimiento de cada tweet
        for index, tweet in fetched_tweets.iterrows(): 
                count+= 1
                parsed_tweet = {}
                # print(tweet[2])
                # almacenamos texto original
                parsed_tweet['text'] = tweet[2]  #coge sólo la columna 'Text'
                
                # almacenamos sentimiento 
                parsed_tweet['sentiment'] = get_tweet_sentiment(tweet[2])  #llama a la función get_tweet_sentiment
                print(count)
                print("------------------")
                #guarda en las listas sentiment_sum cada uno de los valores texto-sentimiento
                sentiment_sum['text'].append(clean_tweet_text(parsed_tweet['text']))
                sentiment_sum['sentiment'].append(parsed_tweet['sentiment'])
        # df = pd.DataFrame.from_dict(sentiment_sum, orient="index")
        # df.to_csv('sentiment_sum.csv')
    except tweepy.TweepError as e: 
        print("Error : " + str(e))     

    #ahora cada uno de nuestros tweets tiene una polaridad asignada
    # sentiment_sum

"""# Paso 4: Copiar sentiment en CSV"""

df = fetched_tweets.assign(sentiment = sentiment_sum['sentiment'])

groupedTweets = df.groupby('sentiment')

positiveTweets=pd.DataFrame()
negativeTweets=pd.DataFrame()
neutralTweets=pd.DataFrame()


for group, i in groupedTweets:
  if group == 'positive': positiveTweets = i
  elif group == 'negative': negativeTweets = i
  elif group == 'neutral': neutralTweets = i

positiveTweets = positiveTweets.reset_index()
negativeTweets = negativeTweets.reset_index()
neutralTweets = neutralTweets.reset_index()

df['sentiment'].value_counts()

positiveTweets.text = positiveTweets.text.apply(
    lambda x:x[2:-1].encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
)
negativeTweets.text = negativeTweets.text.apply(
    lambda x:x[2:-1].encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
)
neutralTweets.text = neutralTweets.text.apply(
    lambda x:x[2:-1].encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
)

stop_words = set(stopwords.words('spanish'))
stop_words.add('https')
stop_words.add('vacuna')
stop_words.add('vacunas')
stop_words.add('co')
stop_words.add('si')
stop_words.add('mas')
stop_words.add('está')
stop_words.add('https co')
stop_words.add('neil young')
stop_words.add('young')
stop_words.add('spotify')
stop_words.add('ad')
stop_words.add('neil')

def remove_Stopwords(text):
  words= word_tokenize(text.lower())
  sentence= [w for w in words if not w in stop_words]
  return " ".join(sentence)

positiveTweets.text= positiveTweets.text.apply(remove_Stopwords)
negativeTweets.text= negativeTweets.text.apply(remove_Stopwords)
neutralTweets.text= neutralTweets.text.apply(remove_Stopwords)

def wordloud(x):
  wordcloud = WordCloud(stopwords=stop_words,collocations=True).generate(' '.join(x))

  plt.figure (figsize=(15,15))
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.show()

wordloud(positiveTweets.text)
wordloud(negativeTweets.text)

union = pd.concat([positiveTweets,negativeTweets])
union['sentiment'].value_counts().plot(kind='bar')

df['sentiment'].value_counts().plot(kind='bar')

def percentage(dividend, divisor):
  return 100 * float(dividend)/float(divisor)

positive = percentage(positiveTweets.shape[0], fetched_tweets.shape[0])
negative = percentage(negativeTweets.shape[0], fetched_tweets.shape[0])
neutral = percentage(neutralTweets.shape[0], fetched_tweets.shape[0])
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
# colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes, startangle=90)
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.legend(labels)
plt.title("Sentiment Analysis Result for vaccines" )
plt.axis('equal')
# p=plt.gcf()
# p.gca().add_artist(my_circle)
plt.show()