from flask_sqlalchemy import SQLAlchemy

# create a DB object
# opening up the db connection
DB = SQLAlchemy()

# Create a table in the DB
# Using Python Classes

class User(DB.Model):
    # for the different columns in out db
    # each one will be its own attribute on this python class

    # ID Column Schema
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column Schema
    username = DB.Column(DB.String, nullable=False)
    # the backref down below automatically adds a list of tweets here
    # tweets = []

class Tweet(DB.Model):
    # ID Column Schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # Test Column Schema
    text = DB.Column(DB.Unicode(300), nullable=False)
    # User Column Scheme
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    # Set up a relationship between tweets and Ids
    # This will automatically add a new id to both the tweet and the user
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)