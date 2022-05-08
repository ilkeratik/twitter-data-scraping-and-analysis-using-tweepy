import pandas as pd
from matplotlib import pyplot as plt
from get_users import *
from get_user_details import *

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
    return df
    
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

def calculate_mean_and_median(tweets, name="user", verbose=False):
    """
    Parameters:
    tweets: tweets
    returns:
    dict of calculations
    """
    df_days = number_of_tweets_per_day(tweets)
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
    mean_per_year = mean_of_tweet_count(df_years)
    median_per_year = median_of_tweet_count(df_years)

    if verbose:
        print(f'mean per day: {mean_per_day}, median per day: {median_per_day}\n \
                mean per week: {mean_per_week}, median per week: {median_per_week}\n \
                mean per month: {mean_per_month}, median per week: {median_per_month}\n \
                mean per year: {mean_per_year}, median per year: {median_per_year}\n \
            ')
    return {name:{'mean per day': mean_per_day, 'median per day': median_per_day, \
            'mean per week': mean_per_week, 'median per week': median_per_week, \
            'mean per month': mean_per_month, 'median per week': median_per_month, \
            'mean per year': mean_per_year, 'median per year': median_per_year}}
    
def save_user_analysis_data_to_csv(tweets, name):
    res = calculate_mean_and_median(tweets)
    df = pd.DataFrame(res).T
    df.index.name = 'Username'
    print(df)
    save_df_to_csv(df, filename='user_analysis_data.csv')

def save_multiple_users_analysis_data_to_csv(users_tweets, users_names):

    for _i, user_tweets in enumerate(users_tweets):
        if _i == 0:
            res = calculate_mean_and_median(user_tweets, name=users_names[_i])
            all_df = pd.DataFrame(res).T
        else:
            print('ger')
            res = calculate_mean_and_median(user_tweets, name=users_names[_i])
            df = pd.DataFrame(res).T
            all_df = all_df.append(df)
    
    all_df.index.name = 'Username'
    print(all_df)
    save_df_to_csv(all_df, filename='multiple_users_analysis_data.csv')
            
def plot_hist(df):
    df.hist()
    plt.show()

def save_df_to_csv(df, filename='Result.csv', index=True):
    df.to_csv(filename, index=index)

if __name__ == '__main__':
    ## single user
    # user = get_user_details("175n07453cr37")
    # idd = user["id"]
    # tweets = get_user_tweets(idd)
    # save_user_analysis_data_to_csv(tweets, name= user['username'])
    ## or multiple users
    users = get_users(query="Kingdom", no_of_users=5)
    print(users)
    users_details = [get_user_details(username) for username in users]
    users_ids = [user['id'] for user in users_details]
    users_tweets = [get_user_tweets(user_id) for user_id in users_ids]
    save_multiple_users_analysis_data_to_csv(users_tweets, users)

