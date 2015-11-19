from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
import ConfigParser

import app.reddit_backend.reddit_helper as r_h

app = Flask(__name__)
app.config.from_object('config')
# SQLAlchemy
db = SQLAlchemy(app)
# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Flask-Bcrypt
bcrypt = Bcrypt(app)
# TODO: Instance per user
reddit = r_h.setup()

from app import views, models
