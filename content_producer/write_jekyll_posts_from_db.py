import mysql.connector
import re
from datetime import datetime


def strip_title(title):
    return title[0:title.find('![')].strip()


def write_post_to_md(post, file, ident_level = 0):
    file.write(f"""<details>
                    <summary>{'> > '*ident_level}{strip_title(post['title'])}</summary>
                    {post['html_body']}
                  </details>""")


def create_post_filename(title, post_time, post_type = 'week'):

    date_regex = r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-)([1-9]|1[0-2])(\.|-)(20)?(1[6-9]|2[0-9])'
    date_finder = re.findall(date_regex, title)

    # if cant find date from title
    if len(date_finder) == 0:
        print("this is not a week message format")
        date_str = post_time.strftime("%Y-%m-%d")
    else:
        first_date_str = ''.join(date_finder[0])
        year_len = len(first_date_str) - first_date_str.rfind('.') - 1
        post_date_from_title = datetime.strptime(first_date_str, f"%d.%m.%{'Y' if year_len == 4 else 'y'}")
        date_str = post_date_from_title.strftime("%Y-%m-%d")

    return f"{date_str}-{post_type}.md"


def generate_childrens_post(posts, parent, tab_offset, file):
    # Get all posts with parent by order. filter & sort
    children_posts = sorted(list(filter(lambda d: d['parent'] == parent, posts)),
                            key=lambda i: i['post_time'])

    # iterate on the the sub posts, for each post print it and call it again for its children
    for post in children_posts:
        write_post_to_md(post, file, tab_offset)
        generate_childrens_post(posts, post['id'], tab_offset + 1, file)


# create the Post page
def generate_header_post(cursor, post):
    cursor.execute((f"""select id, title, post_time, user_name, lesson_code, html_body,parent 
                        from lessons_diary 
                        where root = {post['id']} 
                        order by post_time asc"""))
    posts = list(c.fetchall())

    # create file
    post_filename = create_post_filename(strip_title(post['title']), post['post_time'])
    cur_file_post = open(f'../_posts/lessons_diary/{post_filename}', 'w')

    # add the header
    cur_file_post.write(f"""---
layout: clean-layout
title:  "{strip_title(post['title'])}"
ymonth: {datetime.strftime(post['post_time'], '%Y-%m')}
date:   {datetime.strftime(post['post_time'], '%Y-%m-%d')}
---
""")
    cur_file_post.write(f"# {strip_title(post['title'])} \n")
    cur_file_post.write(post['html_body'] + "\n\n")
    #write_post_to_md(post, cur_file_post)
    generate_childrens_post(posts, post['id'], 0, cur_file_post)

    # add the footer
    cur_file_post.write("""<a href="javascript:history.back()">בית</a>""")

    print(f"Finish writing {post_filename}")
    cur_file_post.close()


if __name__ == '__main__':
    try:
        db = mysql.connector.connect(host='localhost',
                                     user='root',
                                     passwd='example',
                                     db='shambhala')

        c = db.cursor(dictionary=True)
        c.execute("""select id, title, post_time, user_name, lesson_code, html_body,parent 
                     from lessons_diary 
                     where root is null 
                     order by post_time desc""")
        headers = list(c.fetchall())

        for header in headers:
            generate_header_post(c, header)

    except Exception as e:
        print(e)
    finally:
        db.close()
