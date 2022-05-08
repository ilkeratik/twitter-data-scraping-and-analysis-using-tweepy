import tweepy

from scr import *
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
# response = client.search_recent_tweets("Tweepy")
# print(response.meta)

# In this case, the data field of the Response returned is a list of Tweet
# objects
query = "Pandas"
tweets = client.search_recent_tweets(query, user_auth=True,max_results=100,expansions="author_id")
#search_next_token = tweets.meta['next_token']
# Each Tweet object has default ID and text fields
users_name = [user.username for user in tweets.includes['users']]
users = client.get_users(usernames=users_name, user_auth=True, user_fields=["public_metrics","profile_image_url"])
filtered_users = []
counter = 0

while(len(filtered_users) < 50):
    for _i,user in enumerate(users.data):
        if user.public_metrics["followers_count"] > 1000:
            filtered_users.append(user.username)
            counter += 1
        if counter > 50:
            print('found 50 users')
            break
    if (len(filtered_users) < 50):
        print('couldn\'t found 50 users that meets the follower count criteria, seaching again...')
        search_next_token = tweets.meta['next_token']
        tweets = client.search_recent_tweets(query, user_auth=True,expansions="author_id", next_token=search_next_token)
        users_name = [user.username for user in tweets.includes['users']]
        users = client.get_users(usernames=users_name, user_auth=True, user_fields=["public_metrics","profile_image_url"])

print(filtered_users)