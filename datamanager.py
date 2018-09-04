import connection
import time

question_header = ['id','submission_time','view_number','vote_number','title','message','image']
list_header = ['id','submission_time','view_number','vote_number','title']
QUESTION_FILE = "question.csv"

def get_questions():
    list_of_questions = connection.read_file(QUESTION_FILE)
    return list_of_questions


def get_question_by_id(id):
    list_of_question = connection.read_file(QUESTION_FILE)
    for question in list_of_question:
        if question['id'] == id:
            return question


def append_question(dict_to_append):
    dict_to_append['id'] = get_new_id()
    dict_to_append['submission_time'] = get_timestamp()
    connection.append_to_csvfile(QUESTION_FILE, dict_to_append, question_header)


def get_new_id():
    ids = []
    list_of_q = connection.read_file(QUESTION_FILE)
    for dict_of_q in list_of_q:
        ids.append(dict_of_q['id'])
    return len(ids) + 1


def get_timestamp():
    return int(time.time())
