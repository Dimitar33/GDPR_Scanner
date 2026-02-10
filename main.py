from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from database.db import db
import bcrypt


app = Flask(__name__)

## Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret'
db.init_app(app)

from database.models import User, Scan

## Create the tables
with app.app_context():
   # db.drop_all()       # uncomment to reset the
    db.create_all()


## Routes
@app.route("/", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":

        user = db.session.execute(select(User).where(User.email == request.form.get("email"))).scalar_one_or_none()

        if user and bcrypt.checkpw(request.form.get("password").encode('utf-8'), user.password):
            return redirect('scan')
        
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = db.session.execute(select(User).where(request.form.get('email') == User.email)).scalar_one_or_none()

        if email:
            flash('Email already registered.')
            return redirect('/')

        salt = bcrypt.gensalt()
        new_user = User(
            email = request.form.get('email'), 
            password = bcrypt.hashpw(request.form.get("password").encode('utf-8'), salt)  # password hash + salt
        )
    
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template("register.html")


@app.route("/scan")
def scan():
    return render_template("scan.html")


## Run the App
if __name__ == "__main__":
    app.run(debug=True)
