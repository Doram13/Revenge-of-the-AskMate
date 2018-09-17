import connection
import time
from datetime import datetime
from operator import itemgetter

question_header = ['id','submission_time','view_number','vote_number','title','message','image']
list_header = ['id','submission_time','view_number','vote_number','title']
answer_header = ['id','submission_time','vote_number','message','image', 'delete']
answer_header_for_file = ['id','submission_time','vote_number', 'question_id', 'message','image']
QUESTION_FILE = "question.csv"
ANSWER_FILE = 'answer.csv'


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
 """)
    list_of_questions = cursor.fetchall()
    return list_of_questions



def get_answers():
    list_of_answers = connection.read_file(ANSWER_FILE)
    return list_of_answers


@connection.connection_handler
def get_question_by_id(cursor, _id):
    cursor.execute("""
    SELECT * FROM question
    WHERE id= %(_id)s;
    """, {"_id": _id})
    question = cursor.fetchone()
    return question


def append_question(dict_to_append):
    dict_to_append['id'] = get_id(QUESTION_FILE)
    dict_to_append['submission_time'] = get_timestamp()
    dict_to_append['vote_number'] = 0
    dict_to_append['view_number'] = 0
    connection.append_to_csvfile(QUESTION_FILE, dict_to_append, question_header)
    return dict_to_append['id']


def get_id(file):
    ids = []
    list_of_file = connection.read_file(file)
    for dict_of_file in list_of_file:
        ids.append(dict_of_file['id'])
    return len(ids)


def get_timestamp():
    return int(time.time())


def convert_timestamp(convertable):
    for i in convertable:
        i['submission_time'] = datetime.fromtimestamp(int(i['submission_time']))
    return convertable


def get_answers_by_id(_id):
    needed_answers = []
    list_of_answers = connection.read_file(ANSWER_FILE)
    convert_timestamp(list_of_answers)
    for answer in list_of_answers:
        if answer['question_id'] == _id:
            needed_answers.append(answer)
    return needed_answers[::-1]


def append_answer(dict_to_append, question_id):
    dict_to_append['id'] = get_id(ANSWER_FILE)
    dict_to_append['submission_time'] = get_timestamp()
    dict_to_append['vote_number'] = 0
    dict_to_append['question_id'] = question_id
    connection.append_to_csvfile(ANSWER_FILE, dict_to_append, answer_header_for_file)


def increase_view_number(_id):
    list_of_questions = get_questions()
    for question in list_of_questions:
        if question['id'] == _id:
            question['view_number'] = int(question['view_number']) + 1
    connection.update_file(QUESTION_FILE, list_of_questions, question_header)


def update_question(_id, edited_dict):
    list_of_questions = get_questions()
    for question in list_of_questions:
        if question['id'] == _id:
            question.update(edited_dict)
    connection.update_file(QUESTION_FILE, list_of_questions, question_header)


def delete_question(_id):
    new_data = []
    list_of_questions = get_questions()
    for question in list_of_questions:
        if question['id'] != _id:
            new_data.append(question)
    connection.update_file(QUESTION_FILE, new_data, question_header)


def delete_answers(_id):
    new_data = []
    list_of_answers = get_answers()
    for answer in list_of_answers:
        if answer['question_id'] != _id:
            new_data.append(answer)
    connection.update_file(ANSWER_FILE, new_data, answer_header_for_file)


def delete_one_answer(_id):
    new_data = []
    list_of_answers = get_answers()
    for answer in list_of_answers:
        if answer['id'] != _id:
            new_data.append(answer)
    connection.update_file(ANSWER_FILE, new_data, answer_header_for_file)


def order_list_by_key(key, order):
    unordered_list = get_questions()
    for question in unordered_list:
        question['view_number'] = int(question['view_number'])
        question['vote_number'] = int(question['vote_number'])
        question['id'] = int(question['id'])
        question['title'] = question['title'].capitalize()
    reverse = True if order == "desc" else False
    sorted_list = sorted(unordered_list, key=itemgetter(key), reverse=reverse)
    connection.update_file(QUESTION_FILE, sorted_list, question_header)


def change_q_vote(_id, number):
    list_of_questions = get_questions()
    for question in list_of_questions:
        if question['id'] == _id:
            question['vote_number'] = int(question['vote_number']) + number
    connection.update_file(QUESTION_FILE, list_of_questions, question_header)


def change_a_vote(_id, number):
    list_of_answers = get_answers()
    for answer in list_of_answers:
        if answer['id'] == _id:
            answer['vote_number'] = int(answer['vote_number']) + number
    connection.update_file(ANSWER_FILE, list_of_answers, answer_header_for_file)