from flask import Flask, render_template, redirect, request, url_for, session
import datamanager
import utils

app = Flask(__name__)


@app.route('/')
def index():
    questions = datamanager.get_first_five_question()
    main_page = 1
    if not session['user_id']:
        session['user_name'] = 0
        session['user_id'] = 0
    return render_template("list.html",
                           questions=questions,
                           header=datamanager.list_header,
                           main_page=main_page,
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name']
                           )



@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if session['user_id'] != 0:
        if request.method == 'GET':
            return render_template('add-question.html', logged_user=session['user_id'],
                                   logged_user_name=session['user_name'])
        _id = datamanager.append_question(request.form['message'],
                                          request.form['title'],
                                          request.form['image'],
                                          session['user_id'])
        return redirect(url_for('display_question', _id=_id, logged_user=session['user_id'],
                                logged_user_name=session['user_name']))
    else:
        return render_template('login.html', logged_user=session['user_id'],
                               logged_user_name=session['user_name'], error_message=datamanager.error_message)


@app.route('/question/<_id>')
def display_question(_id):
    datamanager.increase_view_number(_id)
    question = datamanager.get_question_by_id(_id)
    answers = datamanager.get_answers_by_id(_id)

    return render_template('display-question.html',
                           answers=answers,
                           question=question,
                           header=datamanager.answer_header,
                           comment_header=datamanager.comment_header,
                           comments=datamanager.get_comments_by_question_id(_id),
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name']

                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if session['user_id'] != 0:
        if request.method == 'GET':
            return render_template('new-answer.html', question_id=question_id, logged_user=session['user_id'],
                                   logged_user_name=session['user_name'])

        datamanager.append_answer(question_id, request.form['message'], request.form['image'], session['user_id'])
        return redirect(url_for('display_question', _id=question_id, logged_user=session['user_id'],
                                logged_user_name=session['user_name']))
    else:
        return render_template('login.html', logged_user=session['user_id'],
                               logged_user_name=session['user_name'])


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    author = datamanager.get_user_name_of_question(question_id)
    if author['user_name'] == session['user_name']:
        if request.method == 'GET':
            question_to_edit = datamanager.get_question_by_id(question_id)
            return render_template('edit-question.html',
                                   question=question_to_edit,
                                   question_id=question_id,
                                   logged_user=session['user_id'],
                                   logged_user_name=session['user_name'])
        else:
            edited_question = request.form.to_dict()
            datamanager.update_question(question_id, edited_question)
            return redirect(url_for('display_question', _id=question_id, logged_user=session['user_id'],
                                    logged_user_name=session['user_name']))
    else:
        return render_template('login.html', error_message=datamanager.error_message_wrong_user)


@app.route('/edit/<question_id>/<answer_id>', methods=['GET', 'POST'])
def edit_answer(answer_id, question_id):
    author = datamanager.get_user_name_of_answer(answer_id)

    if author['user_name'] == session['user_name']:
        if request.method == 'GET':
            answer_to_edit = datamanager.get_answer_answer_id(answer_id)
            return render_template('edit-answer.html',
                                   answer=answer_to_edit,
                                   answer_id=answer_id, logged_user=session['user_id'],
                                   logged_user_name=session['user_name'],
                                   )
        edited_answer = request.form.to_dict()
        datamanager.update_answer(answer_id, edited_answer)
        return redirect(url_for('display_question', _id=question_id, logged_user=session['user_id'],
                                logged_user_name=session['user_name'],
                                ))
    else:
        return render_template('login.html', error_message=datamanager.error_message_wrong_user)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    author = datamanager.get_user_name_of_question(question_id)
    if author['user_name'] == session['user_name']:
        user_of_question = datamanager.get_question_by_id(question_id)
        if session['user_id'] == user_of_question['user_id']:
            datamanager.delete_question(question_id)
            return redirect('/')
        else:
            return render_template('login.html', error_message=datamanager.error_message_wrong_user)
    else:
        return render_template('login.html', error_message=datamanager.error_message_wrong_user)


@app.route('/<question_id>/answer/<_id>/delete')
def delete_answer(question_id, _id):
    author = datamanager.get_user_name_of_answer(_id)
    if author['user_name'] == session['user_name']:
        datamanager.delete_one_answer(_id)
        return redirect(url_for('display_question', _id=question_id))
    else:
        return render_template('login.html', error_message=datamanager.error_message)


@app.route('/list')
def list_all_questions():
    questions = datamanager.get_questions()
    main_page = 0
    return render_template("list.html",
                           questions=questions,
                           header=datamanager.list_header,
                           main_page=main_page,
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name'])


@app.route('/ordered-list')
def order_list():
    main_page = 0
    sorted_list = datamanager.order_list_by_key(request.args['order_by'], request.args['order_direction'])
    return render_template('list.html',
                           questions=sorted_list,
                           header=datamanager.list_header,
                           main_page=main_page,
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name'])

@app.route("/question/<q_id>/<direction>")
def question_vote(q_id, direction):
    if session['user_id'] != 0:
        if direction == 'up':
            datamanager.change_q_vote(q_id, 1)
            datamanager.change_reputation(datamanager.get_user_name_of_question(q_id)['user_name'], 5)
        else:
            datamanager.change_q_vote(q_id, -1)
            datamanager.change_reputation(datamanager.get_user_name_of_question(q_id)['user_name'], -2)
        return redirect(url_for('display_question', _id=q_id))
    else:
        return render_template('login.html', error_message=datamanager.error_message)


@app.route("/question/<q_id>/answer/<a_id>/<direction>")
def answer_vote(a_id, q_id, direction):
    if session['user_id'] != 0:
        if direction == 'up':
            number = 1
            datamanager.change_a_vote(a_id, number)
            datamanager.change_reputation(datamanager.get_user_name_of_answer(a_id)['user_name'], 10)
        else:
            number = -1
            datamanager.change_a_vote(a_id, number)
            datamanager.change_reputation(datamanager.get_user_name_of_answer(a_id)['user_name'], -2)
        return redirect(url_for('display_question', _id=q_id))
    else:
        return render_template('login.html', error_message=datamanager.error_message)


@app.route('/search', methods=['GET', 'POST'])
def search_questions():
    questions = datamanager.search_questions(request.form['search'])
    return render_template('list.html', questions=questions,
                           header=datamanager.list_header,
                           main_page=0,
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name'])


@app.route("/question/<question_id>/add-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if session['user_id'] != 0:
        if request.method == 'GET':
            return render_template('add-comment.html', question_id=question_id, logged_user=session['user_id'],
                                   logged_user_name=session['user_name'])
        message = request.form['message']
        datamanager.add_comment_to_question(question_id, message, session['user_id'])
        return redirect(url_for('display_question', _id=question_id))
    else:
        return render_template('login.html', error_message=datamanager.error_message)


@app.route('/edit/<question_id>/comment/<_id>', methods=['GET', 'POST'])
def edit_comment(question_id, _id):
    author = datamanager.get_user_name_of_comment(_id)
    if author['user_name'] == session['user_name']:
        if request.method == 'GET':
            return render_template('edit-comment.html',
                                   comment=datamanager.get_comment_by_comment_id(_id),
                                   question_id=question_id, logged_user=session['user_id'],
                                   logged_user_name=session['user_name'])
        edited_comment = request.form.to_dict()
        datamanager.edit_comment_by_id(edited_comment, _id)
        return redirect(url_for('display_question', _id=question_id))
    else:
        return render_template('login.html', error_message=datamanager.error_message_wrong_user)


@app.route('/<question_id>/comment/<_id>/delete')
def delete_comment(question_id, _id):
    author = datamanager.get_user_name_of_comment(_id)
    if author['user_name'] == session['user_name']:
        datamanager.delete_one_comment(_id)
        return redirect(url_for('display_question', _id=question_id))
    else:
        return render_template('login.html', error_message=datamanager.error_message_wrong_user)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html', logged_user=session['user_id'],
                               logged_user_name=session['user_name'])
    new_user_name = request.form['user_name']
    if datamanager.check_unique_user_name(new_user_name):
        return render_template('registration.html', logged_user=session['user_id'],
                               logged_user_name=session['user_name'], message="Already exists!")
    hashed = utils.hash_password(request.form['password'])
    datamanager.create_user(new_user_name, hashed)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', logged_user=session['user_id'],
                               logged_user_name=session['user_name'])
    user_name_to_check = request.form['user_name']
    password_to_check = request.form['password']
    hash_to_check = datamanager.get_hash(user_name_to_check)
    try:
        is_verified = utils.verify_password(password_to_check, hash_to_check['hash'])
    except:
        error_message = "Wrong password or User Name"
        return render_template('login.html', error_message=error_message, logged_user=session['user_id'],
                               logged_user_name=session['user_name'])
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
        return render_template('login.html', error_message=error_message, logged_user=session['user_id'],
                               logged_user_name=session['user_name'])


@app.route('/logout')
def logout():
    session['user_id'] = 0
    session['user_name'] = 0
    return redirect('/')


@app.route('/userlist')
def list_all_user():
    return render_template('list_all_user.html',
                           list_of_users=utils.get_readable_date_for_users(datamanager.get_user_infos()),
                           header=datamanager.user_header, logged_user=session['user_id'],
                           logged_user_name=session['user_name'])


@app.route('/question/<question_id>/answer/<answer_id>/accept', methods=['GET', 'POST'])
def accept_answer(answer_id, question_id):
    author = datamanager.get_user_name_of_question(question_id)
    if author['user_name'] == session['user_name']:
        datamanager.accept_answer(answer_id)
        datamanager.change_reputation(datamanager.get_user_name_of_answer(answer_id)['user_name'], 15)
        return redirect(url_for('display_question', _id=question_id))
    else:
        return redirect(url_for('display_question', _id=question_id))


@app.route('/user/<user_id>')
def user_details(user_id):
    questions = datamanager.get_questions_by_user_id(user_id)
    answers = datamanager.get_answers_by_user_id(user_id)
    comments = datamanager.get_comments_by_user_id(user_id)
    return render_template('my_activity.html',
                           questions=questions,
                           answers=answers,
                           comments=comments,
                           logged_user=session['user_id'],
                           logged_user_name=session['user_name'])


if __name__ == "__main__":
    app.secret_key = 'very_secret_secret_key'
    app.run(
        debug=True,
        port=5000
    )
