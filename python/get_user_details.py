from tweepy_utils import *

def get_user_details(username, verbose=False):
    """
    Parameters:
    username: twitter username
    returns
    dict of 
    id, username, displayed name, create_date, description, no of followers, no of following 
    for given username

    """ 
    user = api.get_user(screen_name=username)
    features = ['id', 'username','displayed_name', 'created_at', 'description', 'followers_count' ,"followings_count"]
    values = [user.id,username,user.name,user.created_at,user.description,user.followers_count,user.friends_count]
    dict_user = dict(zip(features, values))
    if verbose:
        print(dict_user)
    return dict_user

def get_user_tweets(idd, verbose=False, count=100):
    """
    Parameters:
    idd: twitter id
    returns 
    tweets of user with given id
    """
    #tweets = client.get_users_tweets(id, user_auth=True, max_results=50)
    tweets = api.user_timeline(user_id=idd,trim_user=True, count=count)
    #print(len(tweets), type(tweets))
    if verbose:
        for tweet in tweets:
            print(
                    f'{tweet.id}, {tweet.created_at}, {tweet.text}, \
                    rt: {tweet.retweet_count}, fav: {tweet.favorite_count} '
                )
    return tweets



if __name__=='__main__':
    idd = get_user_details("175n07453cr37")["id"]
    get_user_tweets(idd)