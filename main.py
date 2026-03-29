from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from database.db import db
from routes.userRoutes import userRoutes
import bcrypt
import json
import bin.scanning as s
from flask_login import login_user, current_user, LoginManager, login_required, logout_user

app = Flask(__name__)

## Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret'
db.init_app(app)

from database.models import User, Scan

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


# ## Routes
app.register_blueprint(userRoutes)


@app.route("/scan", methods=["GET", "POST"])
def scan():

    if request.method == "POST":

        url = request.form.get('url')

        if not url:
            return render_template("scan.html")

        cookies = s.scanning(url)

        # gen AI
        scan_result = {
            "cookies_b_c": cookies[0],
            "cookies_a_c": cookies[1],
            "privacy_policy": cookies[2],
            "security_headers": cookies[3]
        }
        
        new_scan = Scan(
            user_id = current_user.id,
            url = url,
            result = json.dumps(scan_result)  # gen AI
        )

        db.session.add(new_scan)
        db.session.commit()
        print(cookies[3])
        return render_template("results.html", cookies_b_c=cookies[0], cookies_a_c=cookies[1], privacy=cookies[2], security_headers = cookies[3])

    return render_template("scan.html")

@app.route("/results/<int:scan_id>")
def results(scan_id):

    if not scan_id:
        return render_template("results.html")

    scan = db.session.execute(select(Scan).where(Scan.id == scan_id)).scalar_one_or_none()
    scan_results = json.loads(scan.result)

    return render_template("results.html", 
                           cookies_b_c=scan_results["cookies_b_c"], 
                           cookies_a_c=scan_results["cookies_a_c"], 
                           privacy=scan_results["privacy_policy"], 
                           security_headers=scan_results["security_headers"])

@app.route("/history")
@login_required
def history():

    scans = db.session.execute(select(Scan).where(current_user.id == Scan.user_id)).scalars().all().__reversed__()

    return render_template("history.html", scans=scans)

@app.route("/delete/<int:scan_id>")
@login_required
def delete(scan_id):

    scan = db.session.execute(select(Scan).where(Scan.id == scan_id)).scalar_one_or_none()

    db.session.delete(scan)
    db.session.commit()

    return redirect(url_for("history"))

## Run the App
if __name__ == "__main__":
    app.run(debug=True)
