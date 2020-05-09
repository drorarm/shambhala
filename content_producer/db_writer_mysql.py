import pymysql

def insert_post(cursor, post, root = None, parent = None):

    # post_time,user_name, title
    md5_column = f"""{post['post_time']}-{post['user']}-{post['title'].replace("'", "''")}-{root}"""
    statement = f"""INSERT IGNORE INTO lessons_diary
                    (title, post_time, user_name, lesson_code, body, html_body, root, parent,md5_column)
                    VALUES('{post['title'].replace("'", "''")}', '{post['post_time']}', '{post['user']}', 
                            '{post['code'].replace("'", "''") if 'code' in post.keys() else 'NULL'}', 
                            '{post['body'].replace("'", "''")}', 
                            '{post['html_body'].replace("'", "''")}', 
                            {root if root else 'NULL'}, {parent if parent else 'NULL'}, md5('{md5_column}'))"""
    try:
        cursor.execute(statement)
    except Exception as e:
        print(f"The insert statemnent {statement} ; The Error {e}")
        return
    return cursor.lastrowid


def write_posts_to_db(posts):
    try:
        db = pymysql.connect(host='localhost',
                            user='root',
                            passwd='example',
                            db='shambhala',
                            autocommit=True)

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        curr_root = -1
        parent_stack = []
        previous_level = -1
        for post in posts:
            # it's new week
            if post['header_level'] == 0:
                return_id = insert_post(cursor, post)
                curr_root = return_id
                parent_stack.clear()
                parent_stack.append(return_id)
            # it's a son / comment
            elif post['header_level'] > previous_level:
                return_id = insert_post(cursor, post, curr_root, parent_stack[-1])
                parent_stack.append(return_id)
            elif post['header_level'] <= previous_level:
                for n in range(previous_level - post['header_level'] + 1):
                    parent_stack.pop()
                return_id = insert_post(cursor, post, curr_root, parent_stack[-1])
                parent_stack.append(return_id)
            else:
                raise Exception("This is impossible")

            previous_level = post['header_level']
    except Exception as e:
        print(e)
    finally:
        db.close()

'''
CREATE DATABASE shambhala CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci; 

create table lessons_diary 
(
id bigint NOT NULL AUTO_INCREMENT,
title varchar(150) not null,
post_time datetime not null,
user_name varchar(30) not null,
lesson_code varchar(40),
body text,
html_body text,
root bigint,
parent bigint,
md5_column varchar(32) NOT NULL,
PRIMARY KEY lessons_diary_pk(id),
UNIQUE KEY post_uq(md5_column),
KEY idx_parent(root, parent)
);'''
