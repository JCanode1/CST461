

"""
from flask import render_template
from dashboard import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(255))

def display_quiz(quiz_id):
    # Fetch quiz data by ID from the 'quiz' table
    quiz = Quiz.query.get(quiz_id)

    if quiz:
        return render_template('display_quiz.html', quiz=quiz)
    else:
        return "Quiz not found"
"""