from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from os import getenv
from .predict import predict_user


# Create a "factory" for serving up the app when it is launched
def create_app():

    # initializes our flask app
    app = Flask(__name__)

    # configutaion stuff
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')

    # connect our database to our app object
    DB.init_app(app)

    # make our "home" or "root" route
    @app.route('/')
    def root():
        users = User.query.all()
        # do this when somebody hits the home page
        # calls the html template
        return render_template('base.html', title='Home', users=User.query.all())
    
    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.usernames for user in users]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='All users have been updated to include their latest tweets.')

  
    # @app.route('/populate')
    # def populate():
    #     add_or_update_user('ryanallred')
    #     add_or_update_user('nasa')
    #     # ryan = User(id=1, username='Ryan')
    #     # DB.session.add(ryan)
    #     # julian = User(id=2, username='Julian')
    #     # DB.session.add(julian)
    #     # tweet1 = User(id=1, text='tweet text', user=ryan, vect=[1, 2, 3], user_id=1)
    #     # DB.session.add(tweet1)
    #     # tweet2 = User(id=1, text="julian's tweet", user=julian, vect=[1, 2, 3], user_id=2)
    #     # DB.session.add(tweet2)
    #     # DB.session.commit()
    #     return '''Created some users.
    #     <a href='/'>Go to Home</a>
    #     <a href='/populate'>Go to populate</a>'''



    # test another route
    @app.route('/reset')
    def test():
        # removes everything from the DB
        DB.drop_all()
        # creates a new DB with indicated tables
        DB.create_all()
        # create a user object from our .models class
        return render_template('base.html', title='Databse Reset')

    
    # This route is NOT just displaying information
    # This route is going to change our database
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # grab the username that the user has put into the input box
        name = name or request.values["user_name"]

        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User "{name}" was successfully added.'
            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f'Error adding{name}: {e}'
            tweets = []
        else:
            return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare a user to themselves!'
        else: 
            tweet_text = request.values['tweet_text']
            prediction = predict_user(user0, user1, tweet_text)
            message = '''"{}" is more likely to be said
                         by {} than {}.'''.format(tweet_text,
                                                            user1 if prediction else user0,
                                                            user0 if prediction else user1)
        
        return render_template('prediction.html', title = 'Prediction', message=message)



    return app
