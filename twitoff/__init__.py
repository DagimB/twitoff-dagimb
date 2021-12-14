from .app import create_app

# telling flask to use our create_app function (factory) 
# now our app will be names "APP"
APP = create_app()
