from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
from .models import Question, Option, User
import time


main = Blueprint('main', __name__)

TRANSIT_DURATION=300
TIMER_DURATION=10
MAX_HINTS=3
MAX_BARS=8

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
    currentBar = current_user.currentBar

    current_question = Question.query.filter_by(id=currentBar).first()

    # set the options for the current question
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
                          question_number=currentBar,
                          total_questions=MAX_BARS,
                          result=result,
                          is_correct=is_correct,
                          selected_answer=selected_answer,
                          wrong_answer=wrong_answer)


@main.route('/next', methods=['POST'])
def next_question():   
    # redirect to transit timer
    return redirect(url_for('main.transit'))


@main.route('/increment_bar', methods=['POST'])
def increment_bar():   
    # increment to next bar
    current_user.questionNum += 1
    current_user.currentBar += 1
    if current_user.currentBar > 8:
        current_user.currentBar = 1
    current_user.hintNum = 1
    db.session.commit()
    # redirect to transit timer
    return redirect(url_for('main.quiz'))


@main.route('/reset', methods=['POST'])
def reset_quiz():
    # resets quiz back to the beginning
    current_user.questionNum = 1
    current_user.hintNum = 1
    if current_user.id == 1:
        current_user.currentBar = 1
    if current_user.id == 2:
        current_user.currentBar = 1
    if current_user.id == 3:
        current_user.currentBar = 3
    if current_user.id == 4:
        current_user.currentBar = 5
    if current_user.id == 5:
        current_user.currentBar = 7
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

    current_question = Question.query.filter_by(id=current_user.currentBar).first()

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


@main.route('/admin')
def admin():
    print(current_user.isAdmin)

    if current_user.isAdmin:
        team1 = User.query.filter_by(id=2).first()
        team2 = User.query.filter_by(id=3).first()
        team3 = User.query.filter_by(id=4).first()
        team4 = User.query.filter_by(id=5).first()

        team1_prog = team1.questionNum
        team2_prog = team2.questionNum
        team3_prog = team3.questionNum
        team4_prog = team4.questionNum

        bar_dict = {
            1: "Shangri-la",
            2: "Yellow Jacket",
            3: "Lazarus",
            4: "Lucky Duck",
            5: "Violet Crown",
            6: "Latchkey",
            7: "Hotel Vegas",
            8: "Grackle",
        }

        team1_bar = bar_dict[team1.currentBar]
        team2_bar = bar_dict[team2.currentBar]
        team3_bar = bar_dict[team3.currentBar]
        team4_bar = bar_dict[team4.currentBar]


        return render_template("admin.html", team1_prog=team1_prog, team2_prog=team2_prog, team3_prog=team3_prog, team4_prog=team4_prog,
                               team1_bar=team1_bar, team2_bar=team2_bar, team3_bar=team3_bar, team4_bar=team4_bar)
    else:
        return "<p>Go away!</p>"
    