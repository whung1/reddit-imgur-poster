from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
import ConfigParser

app = Flask(__name__)
app.config.from_object('config')
# SQLAlchemy
db = SQLAlchemy(app)
# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Flask-Bcrypt
bcrypt = Bcrypt(app)

from app import views, models
