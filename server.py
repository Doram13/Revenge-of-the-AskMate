from flask import Flask, render_template, redirect, request, url_for
import datamanager


app = Flask(__name__)


@app.route('/')
def index():
    questions = datamanager.get_questions()
    return render_template("list.html",
                           questions = datamanager.convert_timestamp(questions),
                           header = datamanager.list_header)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')

    _id = datamanager.append_question(request.form.to_dict())
    return redirect(url_for('display_question', _id=_id))


@app.route('/question/<_id>')
def display_question(_id):
    datamanager.increase_view_number(_id)
    question = datamanager.get_question_by_id(_id)
    answers = datamanager.get_answers_by_id(_id)
    return render_template('display-question.html',
                           answers = answers,
                           question=question,
                           header = datamanager.answer_header)


@app.route('/question/<question_id>/new-answer',  methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id = question_id)

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


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    datamanager.delete_question(question_id)
    datamanager.delete_answers(question_id)
    return redirect('/')


@app.route('/<question_id>/answer/<_id>/delete')
def delete_answer(_id, question_id):
    datamanager.delete_one_answer(_id)
    return redirect(url_for('display_question', _id=question_id))


@app.route('/list')
def order_list():
    datamanager.order_list_by_key(request.args['order_by'], request.args['order_direction'])
    return redirect('/')


@app.route("/question/<q_id>/up")
def q_up_vote(q_id):
    datamanager.increase_q_vote(q_id)
    return redirect(url_for('display_question', _id=q_id))


@app.route("/question/<q_id>/down")
def q_down_vote(q_id):
    datamanager.decrease_q_vote(q_id)
    return redirect(url_for('display_question', _id=q_id))


@app.route("/question/<q_id>/answer/<a_id>/up")
def a_up_vote(a_id, q_id):
    datamanager.increase_a_vote(a_id)
    return redirect(url_for('display_question', _id=q_id))

@app.route("/question/<q_id>/answer/<a_id>/down")
def a_down_vote(a_id, q_id):
    datamanager.decrease_a_vote(a_id)
    return redirect(url_for('display_question', _id=q_id))


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )