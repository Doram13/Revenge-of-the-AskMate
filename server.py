from flask import Flask, render_template, redirect, request, url_for
import datamanager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = datamanager.convert_timestamp(datamanager.get_questions())
    return render_template("list.html",
                           questions = questions[::-1],
                           header = datamanager.list_header)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    if request.method == 'POST':
        new_dict = request.form.to_dict()
        datamanager.append_question(new_dict)
        _id = datamanager.get_id(datamanager.QUESTION_FILE) - 1
        return redirect(url_for('display_question', _id=_id))


@app.route('/question/<_id>')
def display_question(_id):
    datamanager.increase_view_number(_id)
    question = datamanager.get_question_by_id(_id)
    answers = datamanager.get_answers_by_id(_id)
    return render_template('display-question.html',
                           id=_id,
                           answers = answers,
                           question=question,
                           header = datamanager.answer_header)


@app.route('/question/<question_id>/new-answer',  methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id = question_id)
    elif request.method == 'POST':
        answer = request.form.to_dict()
        datamanager.append_answer(answer,question_id)
        return redirect(url_for('display_question', _id=question_id))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'GET':
        question_to_edit = datamanager.get_question_by_id(question_id)
        return render_template('edit-question.html',
                               question = question_to_edit,
                               question_id = question_id)
    elif request.method == 'POST':
        edited_question = request.form.to_dict()
        datamanager.update_question(question_id, edited_question)
        return redirect(url_for('display_question', _id = question_id))


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )