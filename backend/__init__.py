from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config
from .models import db, init_db, User
import os

app = Flask(__name__, static_folder=os.environ["STATIC_FOLDER_PATH"], template_folder=os.environ["TEMPLATE_FOLDER_PATH"])
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config.from_object(Config)
migrate = Migrate(app, db) #https://qiita.com/svfreerider/items/50c68252c2f119583a28
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for bolt parts of app
from .bolt import bolt as bolt_blueprint
app.register_blueprint(bolt_blueprint)

# blueprint for feedback parts of app
from .feedback import feedback as feedback_blueprint
app.register_blueprint(feedback_blueprint)
