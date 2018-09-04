from flask import Flask, render_template, redirect, request
import connection
import datamanager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = datamanager.get_questions()
    return render_template("list.html", questions = questions, header = datamanager.list_header)

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    if request.method == 'POST':
        return redirect('/')

@app.route('/list/question/<id>')
def display_question(id):
    question = datamanager.get_question_by_id(id)
    return render_template('display-question.html', id=id, question=question, header = datamanager.list_header)



if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )