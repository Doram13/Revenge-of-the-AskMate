from flask import Flask, render_template, redirect, request, url_for
import datamanager


app = Flask(__name__)


@app.route('/')
def index():
    questions = datamanager.first_5_question()
    main_page = 1
    return render_template("list.html",
                           questions = questions,
                           header = datamanager.list_header,
                           main_page = main_page)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    _id = datamanager.append_question(request.form['message'],
                                      request.form['title'],
                                      request.form['image'])
    return redirect(url_for('display_question', _id=_id))


@app.route('/question/<_id>')
def display_question(_id):
    datamanager.increase_view_number(_id)
    question = datamanager.get_question_by_id(_id)
    answers = datamanager.get_answers_by_id(_id)
    return render_template('display-question.html',
                           answers=answers,
                           question=question,
                           header=datamanager.answer_header)


@app.route('/question/<question_id>/new-answer',  methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id=question_id)

    datamanager.append_answer(question_id, request.form['message'], request.form['image'])
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


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    datamanager.delete_question(question_id)
    return redirect('/')


@app.route('/<question_id>/answer/<_id>/delete')
def delete_answer(question_id, _id):
    datamanager.delete_one_answer(_id)
    return redirect(url_for('display_question', _id=question_id))


@app.route('/list')
def list_all_questions():
    questions = datamanager.get_questions()
    main_page = 0
    return render_template("list.html",
                           questions=questions,
                           header=datamanager.list_header,
                           main_page = main_page)

def order_list():
    sorted_list = datamanager.order_list_by_key(request.args['order_by'], request.args['order_direction'])
    return render_template('list.html',
                           questions=sorted_list,
                        header = datamanager.list_header)


@app.route("/question/<q_id>/<direction>")
def question_vote(q_id, direction):
    if direction == 'up':
        datamanager.change_q_vote(q_id, 1)
    else:
        datamanager.change_q_vote(q_id, -1)
    return redirect(url_for('display_question', _id=q_id))


@app.route("/question/<q_id>/answer/<a_id>/<direction>")
def answer_vote(a_id, q_id, direction):
    if direction == 'up':
        number = 1
        datamanager.change_a_vote(a_id, number)
    else:
        number = -1
        datamanager.change_a_vote(a_id, number)
    return redirect(url_for('display_question', _id=q_id))


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )