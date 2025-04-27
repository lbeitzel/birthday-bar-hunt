from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.question', number=currentQ))

@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, isAdmin=current_user.isAdmin)

ANSWERS = {
    "1": "green",
    "2": "blue"
}

OPTIONS = {
    "green": "Green",
    "purple": "Purple", 
    "red": "Red",
    "Yellow": "Yellow"
}

currentQ = 1
hint = 3

@main.route("/q/<number>")
@login_required
def question(number=1):
    if number == str(currentQ):
        return render_template("question.html", number=number, hint=hint, options=OPTIONS)
    else:
        return "Error wrong question page"
    

@main.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
    # if not user or user.password != password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@main.route("/result", methods=["POST"])
@login_required
def result():
    global currentQ
    selected = request.form.get('option')
    
    # Check if an option was selected
    if not selected or selected not in OPTIONS:
        return redirect(url_for('main.question', number=currentQ))
    
    # Get the display name of the option
    option_name = OPTIONS.get(selected)

    # if question was answered correctly, proceed to the next question
    if ANSWERS.get(str(currentQ)) == "":
        currentQ += 1
    
    return render_template('result.html', option=selected, option_name=option_name, q=currentQ)