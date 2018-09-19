import connection
import time
from datetime import datetime
from operator import itemgetter
from psycopg2 import sql

question_header = ['id','submission_time','view_number','vote_number','title','message','image']
list_header = ['id','submission_time','view_number','vote_number','title']
answer_header = ['id','submission_time','vote_number','message','image', 'delete']
answer_header_for_file = ['id','submission_time','vote_number', 'question_id', 'message','image']
QUESTION_FILE = "question.csv"
ANSWER_FILE = 'answer.csv'


@connection.connection_handler
def first_5_question(cursor):
    cursor.execute("""
            SELECT * FROM question
            ORDER BY submission_time DESC LIMIT 5;
    """)
    five_questions = cursor.fetchall()
    return five_questions


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id;
 """)
    list_of_questions = cursor.fetchall()
    return list_of_questions

@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    list_of_answers = cursor.fetchall()
    return list_of_answers


@connection.connection_handler
def get_question_by_id(cursor, _id):
    cursor.execute("""
    SELECT * FROM question
    WHERE id= %(_id)s;      
    """, {"_id": _id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def append_question(cursor, message, title, image):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s);
                    SELECT id FROM question
                    ORDER BY id DESC LIMIT 1;
                    """,
                   {'submission_time': datetime.now(), 'title': title, 'message': message, 'image': image})
    _id = cursor.fetchall()
    return _id[0]['id']


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


@connection.connection_handler
def get_answers_by_id(cursor, _id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE question_id= %(_id)s;
    """, {"_id": _id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def append_answer(cursor, question_id, message, image):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
                    VALUES (%(time)s, 0, %(question_id)s, %(message)s, %(image)s)
                    """,
                   {'time': datetime.now(), 'question_id': question_id, 'message': message, 'image': image})

@connection.connection_handler
def increase_view_number(cursor, _id):
    cursor.execute("""
                    UPDATE question 
                    SET view_number = view_number + 1
                    WHERE id = %(_id)s
                    """,
                   {'_id': _id})


@connection.connection_handler
def update_question(cursor, _id, edited_dict):
    title = edited_dict['title']
    message = edited_dict['message']
    image = edited_dict['image']
    cursor.execute("""
            UPDATE question
            SET title = %(title)s
            WHERE id= %(_id)s;
            
            UPDATE question
            SET message = %(message)s
            WHERE id= %(_id)s;
            
            UPDATE question
            SET image = %(image)s
            WHERE id= %(_id)s;""",
                   {'_id': _id,'title': title, 'message': message, 'image': image})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
    DELETE FROM question
    WHERE id = %(_id)s;""",
                {'_id': question_id})


@connection.connection_handler
def delete_one_answer(cursor, _id):
    cursor.execute("""
    DELETE FROM answer
    WHERE id = %(_id)s;""",
                {'_id': _id})


@connection.connection_handler
def order_list_by_key(cursor, col, order):
    if order == "asc":
        cursor.execute(
                sql.SQL("""
                    SELECT * FROM question
                    ORDER BY {col} ASC;  """,).
                    format(col=sql.Identifier(col))
        )
        new_list = cursor.fetchall()
        return new_list
    elif order == "desc":
        cursor.execute(
            sql.SQL("""
                    SELECT * FROM question
                    ORDER BY {col}  DESC; """, ).
                format(col=sql.Identifier(col))
        )
        new_list = cursor.fetchall()
        return new_list


@connection.connection_handler
def change_q_vote(cursor, _id, number):
    cursor.execute("""
    UPDATE question
    SET vote_number =  vote_number + %(number)s
    WHERE id= %(question_id)s;""",
    {'question_id': _id, 'number': number})


@connection.connection_handler
def change_a_vote(cursor, _id, number):
    cursor.execute("""
        UPDATE answer
        SET vote_number =  vote_number + %(number)s
        WHERE id= %(question_id)s;""",
    {'question_id': _id, 'number': number})