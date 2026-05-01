from flask import Flask
from database.db import db
from routes.userRoutes import userRoutes
from routes.scanRoutes import scanRoutes
from flask_login import LoginManager
from database.models import User

app = Flask(__name__)

## Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret'
db.init_app(app)

## Create the tables
with app.app_context():
    #db.drop_all()       # uncomment to reset the db
    db.create_all()

# Connect the login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

## Routes
app.register_blueprint(userRoutes)
app.register_blueprint(scanRoutes)

## Run the App
if __name__ == "__main__":
    app.run(debug=True)