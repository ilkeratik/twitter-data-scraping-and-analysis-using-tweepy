import pandas as pd
import tweepy
import json
from datetime import datetime
from matplotlib import pyplot as plt
from scr import *

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# username, displayed name, description, no of followers, no of following, birthday, join date, website
# for the last 50 tweets
## no of favorites
## no of retweets
## no of replies


def get_user_details(username):
    user = api.get_user(screen_name=username)
    features = ['id', 'username','displayed_name', 'created_at', 'description', 'followers_count' ,"followings_count"]
    values = [user.id,username,user.name,user.created_at,user.description,user.followers_count,user.friends_count]
    dict_user = dict(zip(features, values))
    print(dict_user)
    return dict_user

def get_user_tweets(idd):
    #tweets = client.get_users_tweets(id, user_auth=True, max_results=50)
    tweets = api.user_timeline(user_id=idd,trim_user=True, count=200)
    print(len(tweets), type(tweets))
    number_of_tweets_per_day(tweets)
    # for tweet in tweets:
    #     print(
    #             f'{tweet.id}, {tweet.created_at}, {tweet.text}, rt: {tweet.retweet_count}, fav: {tweet.favorite_count} '
            
    #         )

def number_of_tweets_per_day(tweets):
    days_dict = {}
    for tweet in tweets:
        dt = tweet.created_at.strftime("%d %B %y")
        if not dt in days_dict:
            days_dict[dt] = 1
        else:
            days_dict[dt] += 1
    
    df = pd.DataFrame.from_dict(days_dict,orient='index', columns=['Tweet Count'])
    
    df.index = pd.to_datetime(df.index)
    new_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
    df = df.reindex(new_date_range, fill_value=0)
    
    df.index.name = 'Date'
    
    calculate_mean_and_median(df)
    save_df_to_csv(df)
    
def mean_of_tweet_count(df):
    mean = df['Tweet Count'].mean()
    return mean

def median_of_tweet_count(df):
    median = df['Tweet Count'].median()
    return median

def convert_index_days_to_weeks(df):
    df.index = df.index.to_period('W')
    df = df.groupby(df.index)['Tweet Count'].sum().reset_index()
    return df

def convert_index_days_to_months(df):
    df.index = df.index.to_period('M')
    df = df.groupby(df.index)['Tweet Count'].sum().reset_index()
    return df

def convert_index_days_to_years(df):
    df.index = df.index.to_period('Y')
    df = df.groupby(df.index)['Tweet Count'].sum().reset_index()
    return df

def calculate_mean_and_median(df_days):
    mean_per_day = mean_of_tweet_count(df_days)
    median_per_day = median_of_tweet_count(df_days)

    df_copy = df_days.copy()
    df_weeks = convert_index_days_to_weeks(df_copy)
    mean_per_week = mean_of_tweet_count(df_weeks)
    median_per_week = median_of_tweet_count(df_weeks)

    df_copy = df_days.copy()
    df_months = convert_index_days_to_months(df_copy)
    mean_per_month = mean_of_tweet_count(df_months)
    median_per_month = median_of_tweet_count(df_months)
   
    df_copy = df_days.copy()
    df_years = convert_index_days_to_years(df_copy)
    print(df_years)
    mean_per_year = mean_of_tweet_count(df_years)
    median_per_year = median_of_tweet_count(df_years)

    print(f'mean per day: {mean_per_day}, median per day: {median_per_day}\n \
            mean per week: {mean_per_week}, median per week: {median_per_week}\n \
            mean per month: {mean_per_month}, median per week: {median_per_month}\n \
            mean per year: {mean_per_year}, median per year: {median_per_year}\n \
        ')

def plot_hist(df):
    df.hist()
    plt.show()

def save_df_to_csv(df, filename='Result.csv'):
    df.to_csv(filename)

idd = get_user_details("175n07453cr37")["id"]
get_user_tweets(idd)