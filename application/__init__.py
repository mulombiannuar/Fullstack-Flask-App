from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate 
from flask_wtf import CSRFProtect
from application.config import DevelopmentConfig, ProductionConfig
from dotenv import load_dotenv
from flask_mail import Mail
import os


# initialize the database object
db = SQLAlchemy()

# initialize the migrate object
migrate = Migrate()

# initialize Flask-Mail for email functionality
mail = Mail()


# load environment variables from .env file
load_dotenv()

def create_app():
    
    # initialize the flask application
    app = Flask(__name__)

    # decide config based on environment
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # initialize the database with app
    db.init_app(app)
    
    # initialize migrate with app and db
    migrate.init_app(app, db)
    
    # initialize the mail with app
    mail.init_app(app) 
    
    csrf = CSRFProtect(app)
    
    # import and register blueprints for modular structure
    from application.views.home import home
    from application.views.auth import auth
    from application.views.user import user
    from application.views.post import post

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/users')
    app.register_blueprint(post, url_prefix='/posts')
    
    from application.models.user import User

    # create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # setup LoginManager for user session management
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'  # redirect to login page if not authenticated
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # define how to load a user from the database
        return User.query.get(int(id))

    return app
