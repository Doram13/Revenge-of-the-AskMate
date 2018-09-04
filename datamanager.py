import connection

question_header = ['id','submission_time','view_number','vote_number','title','message','image']
list_header = ['id','submission_time','view_number','vote_number','title']

def get_questions():
    list_of_questions = connection.read_file('question.csv')
    return list_of_questions
