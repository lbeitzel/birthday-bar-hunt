from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or user.password != password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



# @auth.route('/signup')
# def signup():
#     return render_template("signup.html")

# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     # code to validate and add user to database goes here
#     name = request.form.get('name')
#     password = request.form.get('password')
#     isAdmin = False

#     user = User.query.filter_by(name=name).first() # if this returns a user, then the name already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again
#         flash('Name already exists')
#         return redirect(url_for('auth.signup'))
    
#     # check if user is admin
#     if name.lower() == "lucas":
#         isAdmin = True

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(name=name, password=generate_password_hash(password, method='pbkdf2:sha256'), isAdmin=isAdmin)
#     # new_user = User(name=name, password=password, isAdmin=isAdmin)

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))