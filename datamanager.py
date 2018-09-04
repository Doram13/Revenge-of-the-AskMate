import connection
import time
from datetime import datetime

question_header = ['id','submission_time','view_number','vote_number','title','message','image']
list_header = ['id','submission_time','view_number','vote_number','title']
answer_header = ['id','submission_time','vote_number','message','image']
QUESTION_FILE = "question.csv"
ANSWER_FILE = 'answer.csv'

def get_questions():
    list_of_questions = connection.read_file(QUESTION_FILE)
    convert_timestamp(list_of_questions)
    return list_of_questions[::-1]


def get_question_by_id(id):
    list_of_question = connection.read_file(QUESTION_FILE)
    for question in list_of_question:
        if question['id'] == id:
            return question


def append_question(dict_to_append):
    dict_to_append['id'] = get_id()
    dict_to_append['submission_time'] = get_timestamp()
    dict_to_append['vote_number'] = 0
    dict_to_append['view_number'] = 0
    connection.append_to_csvfile(QUESTION_FILE, dict_to_append, question_header)


def get_id():
    ids = []
    list_of_q = connection.read_file(QUESTION_FILE)
    for dict_of_q in list_of_q:
        ids.append(dict_of_q['id'])
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
