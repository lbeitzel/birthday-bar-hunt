from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from .models import Question, Option
import time


main = Blueprint('main', __name__)

TIMER_DURATION=10
MAX_HINTS=3
MAX_BARS=4

@main.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if current_user.questionNum > MAX_BARS:
        return render_template('quiz_complete.html')
    
    # anticheat, redirects to separate timer page
    if 'timer_end' in session:
        remaining = session['timer_end'] - int(time.time())
        if remaining > 0:
            print("Don't cheat!!!")
            return redirect(url_for('main.timer'))
        

    if 'transit_timer' in session:
        remaining = session['transit_timer'] - int(time.time())
        if remaining > 0:
            print("remaining not expired")
            # If timer still active, go back to timer page
            return redirect(url_for('main.transit'))
    
    result = None
    is_correct = False
    selected_answer = None
    wrong_answer = None

    # Get the current question
    questionNum = current_user.questionNum
    hintNum = current_user.hintNum

    current_question = Question.query.filter_by(id=questionNum).first()

    # set the options for the current question
    # TODO: change for LBBR
    options = Option.query.filter_by(id=1).first()
    question_options = [options.option1, options.option2, options.option3, options.option4, options.option5, options.option6, options.option7, options.option8, options.option9, options.option10, options.option11, options.option12]
    
    
    if request.method == 'POST':
        wrong_answer = False

        selected_answer = request.form.get('answer')
        
        if selected_answer:
            # Check if the answer is correct
            if selected_answer == current_question.answer:
                result = f"Correct! Select \"Next Bar\" to continue!"
                is_correct = True
                session['next_bar_timer'] = int(time.time()) + TIMER_DURATION

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
                session['timer_end'] = int(time.time()) + TIMER_DURATION
    
    return render_template('quiz.html', 
                          question=questionNum,
                          hint=hintNum, 
                          hint1=current_question.hint1, 
                          hint2=current_question.hint2, 
                          hint3=current_question.hint3, 
                          answer=current_question.answer,
                          options=question_options,
                          question_number=questionNum,
                          total_questions=MAX_BARS,
                          result=result,
                          is_correct=is_correct,
                          selected_answer=selected_answer,
                          wrong_answer=wrong_answer)


@main.route('/next', methods=['POST'])
def next_question():
    # increment to next bar
    current_user.questionNum += 1
    current_user.hintNum = 1
    db.session.commit()
    
    # redirect to transit timer
    return redirect(url_for('main.transit'))

@main.route('/reset', methods=['POST'])
def reset_quiz():
    # resets quiz back to the beginning
    current_user.questionNum = 1
    current_user.hintNum = 1
    db.session.commit()

    return redirect(url_for('main.quiz'))


@main.route('/timer')
def timer():
    # Set timer duration
    session['timer_end'] = int(time.time()) + TIMER_DURATION
    return render_template('timer.html')


@main.route('/transit')
@login_required
def transit():
    # Set timer duration
    session['transit_timer'] = int(time.time()) + TIMER_DURATION

    current_question = Question.query.filter_by(id=current_user.questionNum-1).first()

    if current_question and current_question.answer:
        return render_template('transit.html', answer=current_question.answer)
    else:
        return render_template('transit.html', answer=None)


@main.route('/completion')
def completion():
    # Check if timer exists and has expired
    if 'timer_end' in session:
        remaining = session['timer_end'] - int(time.time())
        if remaining > 0:
            print("remaining not expired")
            # If timer still active, go back to timer page
            return redirect(url_for('main.timer'))
        
    if 'transit_timer' in session:
        remaining = session['transit_timer'] - int(time.time())
        if remaining > 0:
            print("remaining not expired")
            # If timer still active, go back to timer page
            return redirect(url_for('main.transit'))
    
    # Clear the timer
    session.pop('timer_end', None)
    session.pop('transit_timer', None)
    return render_template('completion.html')


@main.route('/profile')
@login_required
def profile():
    # anticheat, redirects to separate timer page
    if 'timer_end' in session:
        remaining = session['timer_end'] - int(time.time())
        if remaining > 0:
            print("Don't cheat!!!")
            return redirect(url_for('main.timer'))
    
    return render_template("profile.html", name=current_user.name, isAdmin=current_user.isAdmin)
