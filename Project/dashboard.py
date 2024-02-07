from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://quizUser:password@localhost/Kahoot'
db = SQLAlchemy(app)


import json

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    quizID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    questions = db.Column(db.JSON, nullable=True)
    currentQuestionIndex = db.Column(db.Integer, nullable=True)

class Question(db.Model):
    __tablename__ = 'questions'

    questionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=True)
    answer1 = db.Column(db.String(255), nullable=True)
    answer2 = db.Column(db.String(255), nullable=True)
    answer3 = db.Column(db.String(255), nullable=True)
    answer4 = db.Column(db.String(255), nullable=True)
    question_type = db.Column(db.Integer, nullable=True)  # Ensure this line has the correct attribute name


def display_question(questionID):
    question = Question.query.get(questionID)
    if question:
        return render_template('display_question.html', question=question)
    else:
        return "Question not found"

def display_quiz(quizID):
    quiz = Quiz.query.get(quizID)
    if quiz:
        question_ids = quiz.questions
        questions = Question.query.filter(Question.questionID.in_(question_ids)).all()
        return render_template('display_quiz.html',  quiz=quiz, questions=questions)
    else:
        return "Quiz not found"



@app.route('/')
def hello():
    return render_template('dashboard.html')


@app.route('/start')
def start():
    # Fetch all quiz entries from the 'quiz' table
    quizzes = Quiz.query.all()
    return render_template('start.html', quizzes=quizzes)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        quiz_name = request.form.get('quiz_name')
        new_quiz = Quiz(title=quiz_name)
        db.session.add(new_quiz)
        db.session.commit()
    return render_template('create.html')


@app.route('/quiz/<int:quiz_id>')
def show_quiz(quiz_id):
    return display_quiz(quiz_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)