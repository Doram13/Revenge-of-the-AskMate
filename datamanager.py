import connection

question_header = ['id','submission_time','view_number','vote_number','title','message','image']
list_header = ['id','submission_time','view_number','vote_number','title']
QUESTION_FILE = "question.csv"

def get_questions():
    list_of_questions = connection.read_file(QUESTION_FILE)
    return list_of_questions


def get_new_id():
    ids = []
    list_of_q = connection.read_file(QUESTION_FILE)
    for dict_of_q in list_of_q:
        ids.append(dict_of_q['id'])
    return len(ids) + 1
