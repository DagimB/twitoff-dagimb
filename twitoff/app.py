from flask import Flask, render_template
from .models import DB, User, Tweet


# Create a "factory" for serving up the app when it is launched
def create_app():

    # initializes our flask app
    app = Flask(__name__)

    # configutaion stuff
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # connect our database to our app object
    DB.init_app(app)

    # make our "home" or "root" route
    @app.route('/')
    def root():
        users = User.query.all()
        # do this when somebody hits the home page
        # calls the html template
        return render_template('base.html', users=users)

    # test another route
    @app.route('/test')
    def test():
        # removes everything from the DB
        DB.drop_all()
        # creates a new DB with indicated tables
        DB.create_all()
        # create a user object from our .models class
        ryan = User(id=1, username='ryanallred')
        julian = User(id=2, username='julian')
        dagim = User(id=3, username='dagim')
        # add the user to the database
        DB.session.add(ryan)
        DB.session.add(julian)
        DB.session.add(dagim)
        # save the database
        DB.session.commit()
        # display our new user on the page
        # make some tweets
        tweet1 = Tweet(id=1, text='this is some tweet text', user=ryan)
        tweet2 = Tweet(id=2, text='this is some other tweet text', user=julian)
        tweet3 = Tweet(id=3, text='i dont like to tweet', user=dagim)
        tweet4 = Tweet(id=4, text='hello world', user=ryan)
        tweet5 = Tweet(id=5, text='hello galaxy', user=julian)
        tweet6 = Tweet(id=6, text='hello universe', user=dagim)
        # ass the tweets to the DB session
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.add(tweet3)
        DB.session.add(tweet4)
        DB.session.add(tweet5)
        DB.session.add(tweet6)
        #query to get all users
        users = User.query.all()
        return render_template('base.html', users=users, title='test')

    return app
