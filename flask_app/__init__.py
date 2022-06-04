from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '91ccbe50f8623969238cc96e711fb88f'  # secret key for form submittion , xss protection, cookie hacking
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # for
login_manager.login_message_category = 'info'

from flask_app import routes
