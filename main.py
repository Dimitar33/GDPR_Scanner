from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from database.db import db


app = Flask(__name__)

## Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

from database.models import User, Scan

## Create the tables
with app.app_context():
    #db.drop_all()
    db.create_all()


## Routes
@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        new_user = User(
            email = request.form.get('email'), 
            password = request.form.get("password")
        )

        print(new_user.email, new_user.password)  

        db.session.add(new_user)
        db.session.commit()

        return redirect('scan')

    return render_template("register.html")


@app.route("/scan")
def scan():
    return render_template("scan.html")


## Run the App
if __name__ == "__main__":
    app.run(debug=True)
