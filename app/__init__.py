from flask import Flask, session
from flask_session import Session
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from requests_oauthlib import OAuth2Session
from flask_login import current_user, login_required, LoginManager
from datetime import datetime
# from config import Auth #Contains class Auth
from oauth2client.contrib.flask_util import UserOAuth2
from sqlalchemy.ext.declarative import declarative_base
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sslify import SSLify



#youjunk

app = Flask(__name__)
Bootstrap(app)
# sslify = SSLify(app)


app.config.from_object(Config)
db = SQLAlchemy(app)
from app.models import Channel, Video
migrate = Migrate(app, db)

# sess = tf.Session()
# sess.init_app(app)

# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.session_protection = "strong"
from app.models import Video, Channel

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth
    
from app import routes, models
