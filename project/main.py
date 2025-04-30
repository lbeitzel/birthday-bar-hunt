from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Question


main = Blueprint('main', __name__)

OPTIONS = {
    "green": "Green",
    "purple": "Purple", 
    "red": "Red",
    "yellow": "Yellow",
    "blue": "Blue"
}


@main.route('/')
def index():
    return redirect(url_for('main.question', number=1))

@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, isAdmin=current_user.isAdmin)


@main.route("/q/<number>")
@login_required
def question(number=1):
    # first_q = Question(hint1="What is the Lucas's favorite color?", hint2="Another name for emerald, jade, seafoam?", hint3="What color is grass?", answer="green")
    # db.session.add(first_q)
    # db.session.commit()

    question = Question.query.filter_by(id=number).first()

    if number == str(current_user.questionNum):
        return render_template("question.html", number=current_user.questionNum, hintNum=current_user.hintNum, hint1=question.hint1, hint2=question.hint2, hint3=question.hint3, answer=question.answer, options=OPTIONS)
    else:
        return "Error wrong question page"


@main.route("/result", methods=["POST"])
@login_required
def result():
    selected = request.form.get('option')

    question = Question.query.filter_by(id=current_user.questionNum).first()
    
    correctAns = False

    # Check if an option was selected
    if not selected or selected not in OPTIONS:
        return redirect(url_for('main.question', number=current_user.questionNum))
    
    # Get the display name of the option
    option_name = OPTIONS.get(selected)

    print(f"Correct answer: {question.answer}")
    print(f"Chosen answer: {selected}")

    # if question was answered correctly, proceed to the next question
    if question.answer == selected:
        print("You chose the correct answer!")
        correctAns = True
        # current_user.questionNum += 1
    
    return render_template('result.html', option=selected, option_name=option_name, q=current_user.questionNum, correctAns=correctAns)
