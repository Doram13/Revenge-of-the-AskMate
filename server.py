from flask import Flask, render_template, redirect, request, url_for, session
import datamanager
import utils

app = Flask(__name__)


@app.route('/')
def index():
    questions = datamanager.first_5_question()
    main_page = 1
    return render_template("list.html",
                           questions=questions,
                           header=datamanager.list_header,
                           main_page=main_page
                           )


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    _id = datamanager.append_question(request.form['message'],
                                      request.form['title'],
                                      request.form['image'])
    return redirect(url_for('display_question', _id=_id, logged_user=session['user_id']))


@app.route('/question/<_id>')
def display_question(_id):
    datamanager.increase_view_number(_id)
    question = datamanager.get_question_by_id(_id)
    answers = datamanager.get_answers_by_id(_id)

    return render_template('display-question.html',
                           answers=answers,
                           question=question,
                           header=datamanager.answer_header,
                           comment_header = datamanager.comment_header,
                           comments=datamanager.get_comments_by_question_id(_id),
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name']

                           )


@app.route('/question/<question_id>/new-answer',  methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id=question_id, logged_user=session['user_id'])

    datamanager.append_answer(question_id, request.form['message'], request.form['image'])
    return redirect(url_for('display_question', _id=question_id, logged_user=session['user_id']))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'GET':
        question_to_edit = datamanager.get_question_by_id(question_id)
        return render_template('edit-question.html',
                               question = question_to_edit,
                               question_id=question_id,
                               logged_user=session['user_id'],
                               logged_user_name=session['user_name'])
    elif request.method == 'POST':
        edited_question = request.form.to_dict()
        datamanager.update_question(question_id, edited_question)
        return redirect(url_for('display_question', _id=question_id, logged_user=session['user_id']))


@app.route('/edit/<question_id>/<answer_id>', methods=['GET', 'POST'])
def edit_answer(answer_id, question_id):
    if request.method == 'GET':
        answer_to_edit = datamanager.get_answer_answer_id(answer_id)
        return render_template('edit-answer.html',
                               answer = answer_to_edit,
                               answer_id=answer_id, logged_user=session['user_id'],
                               logged_user_name=session['user_name'])
    edited_answer = request.form.to_dict()
    datamanager.update_answer(answer_id, edited_answer)
    return redirect(url_for('display_question', _id=question_id, logged_user=session['user_id'],
                            logged_user_name=session['user_name']))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    user_of_question = datamanager.get_question_by_id(question_id)
    if session['user_id'] == user_of_question['user_id']:
        datamanager.delete_question(question_id)
        return redirect('/')
    else:
        return redirect(url_for('login'))


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
                           main_page = main_page,
                           logged_user_name=session['user_name'])


@app.route('/ordered-list')
def order_list():
    main_page = 0
    sorted_list = datamanager.order_list_by_key(request.args['order_by'], request.args['order_direction'])
    return render_template('list.html',
                            questions=sorted_list,
                            header = datamanager.list_header,
                            main_page=main_page,
                           logged_user_name=session['user_name'])


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


@app.route('/search', methods = ['GET', 'POST'])
def search_questions():
    questions = datamanager.search_questions(request.form['search'])
    return render_template('list.html', questions = questions,
                                        header = datamanager.list_header,
                                        main_page= 0,
                                        logged_user_name=session['user_name'])


@app.route("/question/<question_id>/add-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template('add-comment.html', question_id=question_id, )
    message = request.form['message']
    datamanager.add_comment_to_question(question_id, message)
    return redirect(url_for('display_question', _id=question_id))


@app.route('/edit/<question_id>/comment/<_id>', methods=['GET', 'POST'])
def edit_comment(question_id, _id):
    if request.method == 'GET':
        return render_template('edit-comment.html',
                               comment = datamanager.get_comment_by_comment_id(_id),
                               question_id=question_id)
    edited_comment = request.form.to_dict()
    datamanager.edit_comment_by_id(edited_comment, _id)
    return redirect(url_for('display_question', _id = question_id))


@app.route('/<question_id>/comment/<_id>/delete')
def delete_comment(question_id, _id):
    datamanager.delete_one_comment(_id)
    return redirect(url_for('display_question', _id=question_id))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    new_user_name = request.form['user_name']
    if datamanager.check_unique_user_name(new_user_name):
        return render_template('registration.html', used_user_name=1)
    hashed = utils.hash_password(request.form['password'])
    datamanager.create_user(new_user_name, hashed)
    return redirect('/')  # TODO: time of registration


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user_name_to_check = request.form['user_name']
    password_to_check = request.form['password']
    hash_to_check = datamanager.get_hash(user_name_to_check)
    try:
        is_verified = utils.verify_password(password_to_check, hash_to_check['hash'])
    except:
        error_message = "Wrong password or User Name"
        return render_template('login.html', error_message=error_message)
    if is_verified == True:
        session['user_id'] = datamanager.get_user_id(user_name_to_check)['user_id']
        session['user_name'] = user_name_to_check
        questions = datamanager.get_questions()
        main_page = 0
        return render_template("list.html",
                               questions=questions,
                               header=datamanager.list_header,
                               main_page=main_page,
                               logged_user=session['user_id'],
                               logged_user_name=session['user_name'])
    else:
        error_message = "Wrong password or User Name"
        return render_template('login.html', error_message=error_message)


@app.route('/logout')
def logout():
    session['user_id'] = None
    session['user_name'] = None
    return redirect('/')


if __name__ == "__main__":
    app.secret_key = 'very_secret_secret_key'
    app.run(
      debug=True,
      port=5000
    )