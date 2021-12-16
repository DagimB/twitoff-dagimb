import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):
    '''
    Determine and returns which user is more likely to say a given tweet
    Example run: predict_user('elonmusk', "jackblack", ""Tesla cars go vroom")
    Returns a 0 (user0_name: "elonmusk") or a 1 (user1_name: "jackblack")
    '''

    # query the database for out two users
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get the numpy array of word embeddings for each user's tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # combine the user's tweet's word embeddings into one big np array
    
    # use vstack to concatenate 2-D numpy arrays
    # X matrix for training
    vects = np.vstack([user0_vects, user1_vects])
    
    # user np.concatenate() to concatenate 1-D numpy arrays
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # y vector for training
    labels = np.concatenate([zeros, ones])


    # Train our logistic regression
    # instantiating the class to create a LR object
    log_reg = LogisticRegression()

    # Fit the model to the data
    log_reg.fit(X=vects, y=labels)

    # generate a prediction for our hypothetical tweet text
    # vectorize my hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # I have to pass in a 2-D numpy array to ,predict()
    prediction = log_reg.predict([hypo_tweet_vect])


    return prediction[0]

# print(predict_user('ryanallred', 'nasa', 'the rocket is going to the moon'))
