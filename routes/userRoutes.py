from flask import Blueprint, render_template, request, redirect, flash, url_for
from sqlalchemy import select
from database.db import db
import bcrypt
from flask_login import login_user, current_user, login_required, logout_user

from database.models import User

userRoutes = Blueprint("userRoutes", __name__)

@userRoutes.route("/", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":

        user = db.session.execute(select(User).where(User.email == request.form.get("email"))).scalar_one_or_none()

        if user and bcrypt.checkpw(request.form.get("password").encode('utf-8'), user.password):
            login_user(user)
            print(user, current_user)
            return redirect(url_for("scanRoutes.scan"))
        
    return render_template("index.html")

@userRoutes.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = db.session.execute(select(User).where(request.form.get('email') == User.email)).scalar_one_or_none()

        if email:
            flash('Email already registered.')
            return redirect('/')

        salt = bcrypt.gensalt()
        update_user = User(
            email = request.form.get("email"), 
            password = bcrypt.hashpw(request.form.get("password").encode('utf-8'), salt)  # password hash + salt
        )
    
        db.session.add(update_user)
        db.session.commit()

        return redirect('/')

    return render_template("register.html")

@userRoutes.route("/userInfo", methods=["GET", "POST"])
@login_required
def userInfo():

    if request.method == "POST":

        button = request.form.get("submit")

        if button == "save": 
            
            update_user = current_user
            update_user.name = request.form.get("name")
            update_user.surname = request.form.get("surname")
            update_user.phone = request.form.get("phone")
            update_user.city = request.form.get("city")
            update_user.country = request.form.get("country")
        
            db.session.add(update_user)
            db.session.commit()
            return render_template("userInfo.html")
        
        elif button == "delete":
        
            user = current_user._get_current_object()
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("userRoutes.login"))
        
    return render_template("userInfo.html")

@userRoutes.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("userRoutes.login"))
