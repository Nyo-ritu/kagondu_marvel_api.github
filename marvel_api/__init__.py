from flask import Flask
from config import Config
from .authentication.routes import auth
from .site.routes import site
from .api.routes import api
from .models import db, User, login_manager, ma
from flask_migrate import Migrate
from .helpers import JSONEncoder
from flask_cors import CORS
app = Flask(__name__)

app.config.from_object(Config)


migrate = Migrate(app, db)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

db.init_app(app)

login_manager.init_app(app)

ma.init_app(app)

login_manager.login_view = 'auth.signin'

app.json_encoder = JSONEncoder

CORS(app)
from .models import User




from .models import db, User