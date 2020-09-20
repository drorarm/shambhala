import mysql.connector
import re
from datetime import datetime


def reformat_date(date_touple, d_format="bens_week"):
    if d_format == "bens_week":
        return "{}{}{}".format(date_touple[0] if len(date_touple[0]) == 2 else "0"+date_touple[0],
                              date_touple[2] if len(date_touple[2]) == 2 else "0"+date_touple[2],
                               ''.join(date_touple[4:]))
    elif d_format == 'drors_day':
        return "{}_{}_{}".format(date_touple[0], date_touple[1], date_touple[2])


def get_lesson_hashtag(title):
    title_fix = title.replace('״', '"')
    code = re.findall(r'"([^"]*)"', title_fix)
    if code:
        return "#שער_קסמים_{0}".format(code[0].replace(' ', '_'))
    else:
        return "#שער_קסמים_{0}".format("קוד_לא_זמיו")

def get_week_hashtag(title):
    pattern = re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-)([1-9]|1[0-2])(\.|-)(20)?(1[6-9]|2[0-9])')
    y = re.findall(pattern, title)

    # שבוע_300820_עד_050920
    fd = reformat_date(y[0])
    td = reformat_date(y[1])
    return "#שבוע_{0}_עד_{1}".format(fd, td)


def get_day_hashtag(title):
    db_date_format = re.compile(r'(201[6-9]|202[0-9])(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])')
    db_date_format2 = re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])([1-9]|1[0-2])(201[6-9]|202[0-9])')
    y = re.findall(db_date_format, title)
     # #יממה_2020_09_03
    if len(y) >= 1:
        return "#יממה_{}".format(reformat_date(y[0], 'drors_day'))

    # try another format
    db_date_format = re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])\.([1-9]|1[0-2])\.(201[6-9]|202[0-9])')
    y = re.findall(db_date_format, title)
    if len(y) >= 1:
        return "#יממה_{}".format(reformat_date(y[0], 'drors_day'))

    # try another format
    db_date_format = re.compile(r'([1-9]|1[0-9]|2[0-9]|3[0-1])\.([1-9]|1[0-2])\.(1[6-9]|2[0-9])')
    y = re.findall(db_date_format, title)
    if len(y) >= 1:
        return "#יממה_{}".format(reformat_date(y[0], 'drors_day'))

    return ""


if __name__ == '__main__':
    try:
        # tapuzUser = "DrorKFTC"
        tapuzUser = "בהתחלה"
        db = mysql.connector.connect(host='localhost',
                                     user='root',
                                     passwd='example',
                                     db='shambhala')

        c = db.cursor(dictionary=True)
        # c.execute(f"""select ben.title as week_title, dror.title as lesson_title, dror.body as lessons_body
        #             from
        #             (select title,body, parent from lessons_diary where user_name = '{tapuzUser}') dror
        #             join
        #             (select id, title from lessons_diary
        #             where root is null
        #             and user_name in ('הדרכה פלאית', 'ידע פלאי')
        #             and post_time > '2017-09-01'
        #             and id > 1) ben on dror.parent = ben.id""")
        c.execute(f"""select weeks.title as week_title, reebLessons.title as lesson_title, reebLessons.body as lessons_body 
                        from
                        (select id as reebRoot ,root as benRoot 
                        from lessons_diary 
                        where user_name = '{tapuzUser}' and root = parent and post_time >= '2017-10-30 08:47:00') reeb
                        join 
                        (select id, title from lessons_diary 
                        where root is null 
                        and user_name in ('הדרכה פלאית', 'ידע פלאי')
                        and post_time > '2016-03-21 17:11:00'
                        and id > 1) weeks on (reeb.benRoot = weeks.id)
                        join 
                        (select * from lessons_diary 
                        where user_name = '{tapuzUser}') reebLessons on (reebLessons.parent = reeb.reebRoot)""")
        posts = list(c.fetchall())

        print(len(posts))
        post_file = open(f'../facebook/{tapuzUser}.txt', 'w')

        for post in posts:
            lesson_hashtag = get_lesson_hashtag(post['lesson_title'])
            week_hashtag = get_week_hashtag(post['week_title'])
            day_hashtag = get_day_hashtag(post['lesson_title'])

            print(day_hashtag if day_hashtag else post['lesson_title'])

            post_file.write(f"\n{post['lessons_body']}\n\n")
            post_file.write(f'{week_hashtag}')
            post_file.write(f'\n{lesson_hashtag}')
            post_file.write(f'\n{day_hashtag}\n')
            post_file.write("#שחזור_מגיבוי")
            post_file.write('\n\n-----------------------------------------------------------------------------------')
            print("-----------------------------------------------------------------------------------")


    except Exception as e:
        print(e)
    finally:
        db.close()
        post_file.close()
