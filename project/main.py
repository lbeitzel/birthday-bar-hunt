from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from .models import Question, Option
import time


main = Blueprint('main', __name__)



# Quiz questions
# quiz_questions = [
#     {
#         "question": "What is the capital of France?",
#         "options": ["London", "Berlin", "Paris", "Madrid"],
#         "correct_answer": "Paris"
#     },
#     {
#         "question": "Which planet is known as the Red Planet?",
#         "options": ["Venus", "Mars", "Jupiter", "Saturn"],
#         "correct_answer": "Mars"
#     },
#     # {
#     #     "question": "What is the largest ocean on Earth?",
#     #     "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
#     #     "correct_answer": "Pacific Ocean"
#     # },
#     # {
#     #     "question": "What is the chemical symbol for gold?",
#     #     "options": ["Go", "Gd", "Au", "Ag"],
#     #     "correct_answer": "Au"
#     # },
#     # {
#     #     "question": "Who painted the Mona Lisa?",
#     #     "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
#     #     "correct_answer": "Leonardo da Vinci"
#     # }
# ]

timer_duration=5
MAX_HINTS=3
MAX_BARS=2

@main.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    # Initialize session variables if they don't exist
    # if 'current_question' not in session:
    #     session['current_question'] = 0
        # session['correct_count'] = 0
        # session['total_questions'] = len(quiz_questions)
    
    # Check if we've completed all questions
    # if session['current_question'] >= len(quiz_questions):
    # if session['current_question'] >= quiz_questions:
        # Quiz is complete, show results
        # correct_count = session['correct_count']
        # total_questions = session['total_questions']
        # Reset the quiz
        # session.pop('current_question', None)
        # session.pop('correct_count', None)
        # session.pop('total_questions', None)
    if current_user.questionNum > MAX_BARS:
        return render_template('quiz_complete.html')
    
    if 'timer_end' in session:
        remaining = session['timer_end'] - int(time.time())
        if remaining > 0:
            print("Don't cheat!!!")
            # If timer still active, go back to timer page
            return redirect(url_for('main.timer'))
    
    
    result = None
    is_correct = False
    selected_answer = None
    wrong_answer = None

    # Get the current question
    questionNum = current_user.questionNum
    hintNum = current_user.hintNum
    # current_q_index = session['current_question']
    # print(current_q_index)
    # current_question = quiz_questions[current_q_index]
    # current_question = str(Question.query.filter_by(id=current_q_index).first())
    current_question = Question.query.filter_by(id=questionNum).first()
    # current_hint = current_question.hint1
    # question = Question.query.filter_by(id=number).first()
    options = Option.query.filter_by(id=current_user.id).first()
    question_options = [options.option1, options.option2, options.option3, options.option4, options.option5]
    

    # if number == str(current_user.questionNum):
    #      render_template("question.html", number=current_user.questionNum, hintNum=current_user.hintNum, hint1=question.hint1, hint2=question.hint2, hint3=question.hint3, answer=question.answer, options=question_options)
    
    if request.method == 'POST':
        wrong_answer = False

        selected_answer = request.form.get('answer')
        
        if selected_answer:
            # Check if the answer is correct
            print(f"selected answer: {selected_answer}")
            print(f"real answer: {current_question.answer}")
            if selected_answer == current_question.answer:
            # if selected_answer == question:
                result = "Correct! Click Next to continue."
                is_correct = True
                # session['correct_count'] = session.get('correct_count', 0) + 1

            else:
                result = f"Incorrect. Try again!"
                # display timer
                wrong_answer = True
                # increment the current hint
                current_user.hintNum += 1
                if current_user.hintNum > MAX_HINTS: 
                    current_user.hintNum = 3
                db.session.commit()

                # Set timer duration to 10 seconds
                session['timer_end'] = int(time.time()) + timer_duration

    print(current_question.hint1)
    print(current_question.hint2)
    print(current_question.hint3)
    
    return render_template('quiz.html', 
                          question=questionNum,
                          hint=hintNum, 
                          hint1=current_question.hint1, 
                          hint2=current_question.hint2, 
                          hint3=current_question.hint3, 
                          answer=current_question.answer,
                        #   options=current_question["options"],
                          options=question_options,
                          question_number=questionNum,
                        #   total_questions=len(quiz_questions),
                          total_questions=MAX_BARS,
                          result=result,
                          is_correct=is_correct,
                          selected_answer=selected_answer,
                          wrong_answer=wrong_answer)


@main.route('/next', methods=['POST'])
def next_question():
    # Move to the next question
    # if 'current_question' in session:
    #     session['current_question'] = session['current_question'] + 1
    # else:
    #     session['current_question'] = 0

    # increment to next bar
    current_user.questionNum += 1
    current_user.hintNum = 1
    # if current_user.questionNum > MAX_BARS: 
    #     current_user.questionNum = 1
    db.session.commit()
    
    
    # Make sure the changes are saved to the session
    session.modified = True
    
    return redirect(url_for('main.quiz'))

@main.route('/reset', methods=['POST'])
def reset_quiz():
    # Reset the quiz
    session.pop('current_question', None)
    session.pop('correct_count', None)
    session.pop('total_questions', None)

    current_user.questionNum = 1
    current_user.hintNum = 1
    db.session.commit()

    return redirect(url_for('main.quiz'))


# @main.route('/')
# def index():
#     # return redirect(url_for('main.question', number=1))
#     return render_template('index.html')

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

    if 'timer_end' in session:
        remaining = session['timer_end'] - int(time.time())
        if remaining > 0:
            print("Don't cheat!!!")
            # If timer still active, go back to timer page
            return redirect(url_for('main.timer'))

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


@main.route('/timer')
def timer():
    # Set timer duration
    session['timer_end'] = int(time.time()) + timer_duration
    return render_template('timer.html')


@main.route('/completion')
def completion():
    # Check if timer exists and has expired
    if 'timer_end' in session:
        remaining = session['timer_end'] - int(time.time())
        if remaining > 0:
            print("remaining not expired")
            # If timer still active, go back to timer page
            return redirect(url_for('main.timer'))
    
    # Clear the timer
    session.pop('timer_end', None)
    return render_template('completion.html')
