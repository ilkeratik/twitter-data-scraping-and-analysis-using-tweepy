from user_tweet_data_analysis import *
from get_users import *
from get_user_details import *

if __name__ == '__main__':
    ## single user
    # user = get_user_details("175n07453cr37")
    # idd = user["id"]
    # tweets = get_user_tweets(idd)
    # save_user_analysis_data_to_csv(tweets, name= user['username'])
    ## or multiple users
    users = get_users(query="Kingdom", no_of_users=50)
    print(users)
    users_details = [get_user_details(username) for username in users]
    users_ids = [user['id'] for user in users_details]
    users_tweets = [get_user_tweets(user_id) for user_id in users_ids]
    save_multiple_users_analysis_data_to_csv(users_tweets, users, users_details)