from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import *
from .routes import ROUTES as blueprints

for blueprint, prefix in blueprints:
    if prefix:
        app.register_blueprint(blueprint, url_prefix=prefix)
        continue
    app.register_blueprint(blueprint)
