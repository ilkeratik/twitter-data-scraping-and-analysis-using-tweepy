from tweepy_utils import *

def get_users(query = "Pandas", verbose = False, no_of_users=50):

    tweets = client.search_recent_tweets(query, user_auth=True,max_results=100,expansions="author_id")
    #search_next_token = tweets.meta['next_token']
    users_name = [user.username for user in tweets.includes['users']]

    users = client.get_users(usernames=users_name, user_auth=True, user_fields=["public_metrics"])
    filtered_users = []
    counter = 0

    while(len(filtered_users) < no_of_users):
        for _i,user in enumerate(users.data):
            # taking users that has over 1k follower only
            if user.public_metrics["followers_count"] > 1000:
                filtered_users.append(user.username)
                counter += 1
            # getting {no_of_users} random user, check if already found enough
            if counter > no_of_users:
                print(f'found {no_of_users} users')
                break
        # if not found enough users in the search, jump to next page of results.
        if (len(filtered_users) < no_of_users):
            print(f'couldn\'t found {no_of_users} users that meets the follower count criteria, seaching next page...')
            search_next_token = tweets.meta['next_token']
            tweets = client.search_recent_tweets(query, user_auth=True,expansions="author_id", next_token=search_next_token)
            users_name = [user.username for user in tweets.includes['users']]
            users = client.get_users(usernames=users_name, user_auth=True, user_fields=["public_metrics"])
    if verbose:
        print(filtered_users)
    
    return filtered_users