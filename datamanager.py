import connection
import utils
from datetime import datetime
from psycopg2 import sql

list_header = ['ID', 'submission_time', 'view_number', 'vote_number', 'title']
answer_header = ['ID', 'submission time', 'vote number', 'message', 'image', 'delete', 'edit', 'accepted']
error_message = "You are not allowed to modify this, because you're not the author of it."
comment_header = ["message", "submission time", 'edited number']
user_header = ['ID', 'Name', 'Registered:', 'Reputation']

@connection.connection_handler
def first_5_question(cursor):
    cursor.execute("""
            SELECT * FROM question
            ORDER BY submission_time DESC LIMIT 5;
    """)
    five_questions = cursor.fetchall()
    return utils.get_readable_date(five_questions)


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id;
 """)
    list_of_questions = cursor.fetchall()
    return utils.get_readable_date(list_of_questions)


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    list_of_answers = cursor.fetchall()
    return utils.get_readable_date(list_of_answers)


@connection.connection_handler
def get_question_by_id(cursor, _id):
    cursor.execute("""
    SELECT * FROM question
    WHERE id= %(_id)s;      
    """, {"_id": _id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_user_id_of_question(cursor, question_id):
    cursor.execute("""
    SELECT user_id FROM question
    WHERE id=%(question_id)s;""", {"question_id": question_id}

                   )


@connection.connection_handler
def append_question(cursor, message, title, image, user_id):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s, %(user_id)s);
                    SELECT id FROM question
                    ORDER BY id DESC LIMIT 1;
                    """,
                   {'submission_time': datetime.now(), 'title': title, 'message': message, 'image': image,
                    'user_id': user_id})
    _id = cursor.fetchall()
    return _id[0]['id']


@connection.connection_handler
def get_answers_by_id(cursor, _id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE question_id= %(_id)s ORDER BY id DESC;
    """, {"_id": _id})
    answers = cursor.fetchall()
    return utils.get_readable_date(answers)


@connection.connection_handler
def get_answer_answer_id(cursor, _id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE id= %(_id)s;
    """, {"_id": _id})
    answer = cursor.fetchone()
    return answer


@connection.connection_handler
def append_answer(cursor, question_id, message, image, user_id):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id, accepted) 
                    VALUES (%(time)s, 0, %(question_id)s, %(message)s, %(image)s, %(user_id)s, FALSE )
                    """,
                   {'time': datetime.now(), 'question_id': question_id, 'message': message, 'image': image,
                    'user_id': user_id})


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
            SET title = %(title)s, message =%(message)s, image = %(image)s
            WHERE id= %(_id)s;
                    """,
                   {'_id': _id, 'title': title, 'message': message, 'image': image})


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
                    ORDER BY {col} ASC;  """, ).
                format(col=sql.Identifier(col))
        )
        new_list = cursor.fetchall()
        return utils.get_readable_date(new_list)
    elif order == "desc":
        cursor.execute(
            sql.SQL("""
                    SELECT * FROM question
                    ORDER BY {col}  DESC; """, ).
                format(col=sql.Identifier(col))
        )
        new_list = cursor.fetchall()
        return utils.get_readable_date(new_list)


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


@connection.connection_handler
def search_questions(cursor, searched_term):
    cursor.execute("""
                    SELECT question.* FROM question
                    LEFT JOIN answer a on question.id = a.question_id
                    WHERE title LIKE %(word)s 
                    OR question.message like %(word)s
                    OR a.message LIKE %(word)s;
                    
                    """, {'word': '%' + searched_term + '%'})
    questions = cursor.fetchall()
    return utils.get_readable_date(questions)


@connection.connection_handler
def update_answer(cursor, answer_id, edited_answer):
    message = edited_answer['message']
    image = edited_answer['image']
    cursor.execute("""
                UPDATE answer
                SET message = %(message)s, image = %(image)s
                WHERE id= %(_id)s;
                        """,
                   {'_id': answer_id, 'message': message, 'image': image})


@connection.connection_handler
def get_comments_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s
                    ORDER BY id;
 """, {'question_id': question_id})
    list_of_comments = cursor.fetchall()
    return utils.get_readable_date(list_of_comments)


@connection.connection_handler
def get_comment_by_comment_id(cursor, _id):
    cursor.execute("""
    SELECT id, message FROM comment
    WHERE id = %(_id)s
    """, {'_id': _id})
    comment = cursor.fetchone()
    return comment


@connection.connection_handler
def edit_comment_by_id(cursor, edited_comment, _id):
    message = edited_comment['message']
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s, edited_count = edited_count + 1
                    WHERE id = %(_id)s;
                            """,
                   {'_id': _id, 'message': message})


@connection.connection_handler
def add_comment_to_question(cursor, question_id, message, user_id):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count, user_id)
                    VALUES (%(question_id)s, %(message)s, %(time)s, 0, %(user_id)s)
 """,
                   {'question_id': question_id, 'message': message, 'time': datetime.now(), 'user_id': user_id})


@connection.connection_handler
def delete_one_comment(cursor, _id):
    cursor.execute("""
    DELETE FROM comment
    WHERE id = %(_id)s;""",
                   {'_id': _id})


@connection.connection_handler
def create_user(cursor, new_user_name, hashed):
    cursor.execute("""
    INSERT INTO "user" (user_name, hash, date) 
            VALUES (%(new_user_name)s,%(hashed)s, %(time)s)
                    """,
                   {'new_user_name': new_user_name, 'hashed': hashed, 'time': datetime.now()})


@connection.connection_handler
def get_hash(cursor, user_name):
    cursor.execute("""
    SELECT hash FROM "user"
    WHERE user_name = %(user_name)s
    """, {'user_name': user_name})
    hash_of_user = cursor.fetchone()
    return hash_of_user


@connection.connection_handler
def get_user_id(cursor, user_name):
    cursor.execute("""
    SELECT user_id FROM "user"
    WHERE user_name = %(user_name)s
    """, {'user_name': user_name})
    user_id = cursor.fetchone()
    return user_id


@connection.connection_handler
def check_unique_user_name(cursor, user_name):
    cursor.execute("""
    SELECT user_name FROM "user"
    WHERE user_name= %(user_name)s""", {'user_name': user_name})
    user_exist = cursor.fetchone()
    if user_exist:
        return True
    else:
        return False


@connection.connection_handler
def get_user_name_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT user_name FROM "user"
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    user_name = cursor.fetchone()
    return user_name


@connection.connection_handler
def get_user_name_of_question(cursor, question_id):
    cursor.execute("""
                    SELECT "user".user_name FROM "user"
                    JOIN question ON question.user_id="user".user_id
                    WHERE question.id = %(question_id)s """, {'question_id': question_id})
    author = cursor.fetchone()
    return author


@connection.connection_handler
def get_user_name_of_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT "user".user_name FROM "user"
                    FULL JOIN answer ON answer.user_id="user".user_id
                    WHERE answer.id = %(answer_id)s """, {'answer_id': answer_id})
    author = cursor.fetchone()
    return author


@connection.connection_handler
def get_user_infos(cursor):
    cursor.execute("""
                    SELECT * FROM "user"
                    ORDER BY user_id
                    """)
    users = cursor.fetchall()
    return users


@connection.connection_handler
def get_user_name_of_comment(cursor, _id):
    cursor.execute(""" 
    SELECT "user".user_name FROM "user"
    FULL JOIN comment ON comment.id="user".user_id
    WHERE comment.id = %(_id)s """, {'_id': _id})
    author = cursor.fetchone()
    return author


@connection.connection_handler
def accept_answer(cursor, a_id):
    cursor.execute("""
    UPDATE answer
    SET accepted = TRUE
    WHERE id=%(a_id)s
    """, {'a_id': a_id})


@connection.connection_handler
def change_reputation(cursor, user_name, change):
    cursor.execute("""
    UPDATE "user"
    SET reputation = %(change)s
    WHERE user_name = %(user_name)s
    """, {'change': change, 'user_name': user_name})
