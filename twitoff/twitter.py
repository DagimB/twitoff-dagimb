from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy


# Get our API keys from our .env file
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


# Add a new user to the databse if they don't alreadt exist
# If the user already exists in the DB, just grab their most recent tweets
# that we don't alreadt have and add them to the DB.

def add_or_update_user(username):
    '''Takes username (twitter handle) and pulls user and tweet data
    from the twitter API. THat data should get added to our databse.'''

    try:
        # Get the user data
        twitter_user = TWITTER.get_user(screen_name=username)
        # Create a db_user from my db model
        # Check to see if the database user alreadt exists or not
        # If the user already exists, use the already existing user
        # If the user *doesn't* already exist, make a new one to use
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username))

        # Add the user to the databse
        DB.session.add(db_user)

        # Get the user's tweets
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id = db_user.newest_tweet_id)

        # Check to see if the newest tweet in the DB is equal to
        # the newest tweet from the twitter API
        # if they are the same then we shouldn't add any new tweets.
        # If they are different then we should only add the newsest tweets that
        # have been tweeted since we last saved to the DB.

        # Setting the newest tweets
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Pull out only the tweet information that we care about from the list of tweets
        # Get our vectorization (word embeddings)
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect = tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print(f"Error Processing {username}: {e}")
        # Make sure my whole application knows about error
        raise e
    else: 
        # Save the user and all of the tweets that were added to the DB.Session
        DB.session.commit()


nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    # return the word embedding for a griven string of text
    return nlp(tweet_text).vector
