from flask import Flask, render_template, request, redirect, url_for, session
import json

with open('data/questions.json','r', encoding="utf-8") as f:
    questions = json.load(f)
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_question' not in session:
        session['current_question'] = 0
        session['score'] = 0
    if request.method == 'POST':
        current_index = session['current_question']
        selected = request.form.get('answer')
        if selected == questions[current_index]['answer']:
            session['score'] += questions[current_index]['points']
        session['current_question'] += 1

    if session['current_question'] >= len(questions):
        score = session['score']
        session.clear()
        return redirect(url_for('result', score=score))

    current_question = questions[session['current_question']]
    return render_template('quiz.html', question=current_question)

@app.route('/result')
def result():
    score = request.args.get('score', 0)
    return f"<h1>Your result: {score} score!</h1>"

if __name__ == '__main__':
    app.run(debug=True)