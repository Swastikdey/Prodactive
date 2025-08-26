from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env


app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Flask-Mail config (use Gmail for example)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail = Mail(app)

from project.models import User

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # route name of login view
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
