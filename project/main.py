from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Question, Option


main = Blueprint('main', __name__)

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
    # ### method for creating a new DB via model definition
    # options = Option(option1="Green", option2="Purple", option3="Red", option4="Yellow", option5="Blue")
    # db.session.add(options)
    # db.session.commit()

    question = Question.query.filter_by(id=number).first()
    options = Option.query.filter_by(id=current_user.id).first()
    question_options = [options.option1, options.option2, options.option3, options.option4, options.option5]

    if number == str(current_user.questionNum):
        return render_template("question.html", number=current_user.questionNum, hintNum=current_user.hintNum, hint1=question.hint1, hint2=question.hint2, hint3=question.hint3, answer=question.answer, options=question_options)
    else:
        return "Error wrong question page"


@main.route("/result", methods=["POST"])
@login_required
def result():
    selected = request.form.get('option')
    question = Question.query.filter_by(id=current_user.questionNum).first()
    correctAns = False
    
    print(f"Correct answer: {question.answer}")
    print(f"Chosen answer: {selected}")

    # if question was answered correctly, proceed to the next question
    if question.answer == selected:
        print("You chose the correct answer!")
        correctAns = True
        # current_user.questionNum += 1
    
    return render_template('result.html', choice=selected, q=current_user.questionNum, correctAns=correctAns)
