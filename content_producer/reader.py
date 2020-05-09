import codecs
import re
import datetime
import html2text


# MTbl is the line that is the header
def decode_mtbl(mtbl, htmler):
    if not mtbl.startswith("MTbl"):
        return False
    mtbl_args = mtbl[5:-3].split(',')

    decoded = {}
    decoded['title'] = htmler.handle(','.join(mtbl_args[6: 7 + (len(mtbl_args) - 14)]).strip('\"'))
    decoded['title'] = decoded['title'].strip('\n')
    decoded['user'] = mtbl_args[-1].strip('\"')
    decoded['header_level'] = int(abs(int(mtbl_args[2]) - 90) / 2)

    extract_post_time = mtbl_args[-2].strip('\"') + " " + mtbl_args[-3].strip('\"')
    decoded['post_time'] = datetime.datetime.strptime(extract_post_time, '%d/%m/%y %H:%M')

    if decoded['header_level'] == 1:
        code = re.findall(r'"([^"]*)"', decoded['title'])
        decoded['code'] = code[0] if code else "Code Missing"

    return decoded


# MArr is the content body of the massage
def extract_body(marr):
    if not marr.startswith("MArr"):
        return False

    marr_args = marr[5:-4].split(',') if isinstance(marr, str) else marr.decode(encoding='cp1255')[5:-4].split(',')
    return ','.join(marr_args[3: 4 + (len(marr_args) - 5)]).strip('\"')


def read_response(respnse_text):
    lines = []
    for line in respnse_text.split('\r\n'):
        if line.startswith("MArr") or line.startswith("MTbl"):
            #print html2text(line)
            lines.append(line)
    posts = []
    htmler = html2text.HTML2Text()
    try:
        line_index = 0
        while line_index < len(lines):
            mtbl = lines[line_index + 1]
            post_dict = decode_mtbl(mtbl, htmler)
            marr = lines[line_index]
            try:
                post_dict['html_body'] = extract_body(marr)
                post_dict['body'] = htmler.handle(post_dict['html_body'])
                posts.append(post_dict)
            except Exception as e:
                print("could not decode html: ")
                print(e)
            line_index = line_index + 2
    except Exception as e:
        print(e)
    finally:
        return posts


def write_posts_to_file(posts, filename='output.txt'):

    file = codecs.open(filename, "w", "utf")
    for post in posts:
        file.write(post['title'] + '\n')
        file.write(u'user:' + post['user'] + '\n')
        file.write(u'post_time: {}\n'.format(post['post_time']))
        file.write(u'header_level: {}\n'.format(post['header_level']))
        file.write("####################\n")
        file.write(post['body'] + '\n')
        file.write("-------------------------------------------------------------------------------------------------------------------------\n")
    file.close()


def main():
    lines = []
    with codecs.open('a01.htm', encoding='cp1255') as f:
        for line in f:
            if line.startswith("MArr") or line.startswith("MTbl"):
                #print html2text(line)
                lines.append(line)

    file = codecs.open("output.txt", "w", "utf")
    posts = []

    try:
        line_index = 0
        while line_index < len(lines):
            mtbl = lines[line_index + 1]
            post_dict = decode_mtbl(mtbl)
            file.write(post_dict['title'] + '\n')
            file.write(u'user:' + post_dict['user'] + '\n')
            file.write(u'post_time: {}\n'.format(post_dict['post_time']))
            file.write(u'header_level: {}\n'.format(post_dict['header_level']))
            file.write("####################\n")

            marr = lines[line_index]
            try:
                content = html2text(extract_body(marr).encode(encoding='cp1255')).decode(encoding='cp1255')
                post_dict['content'] = content
                posts.append(post_dict)
                file.write(content + '\n')
            except Exception as e:
                print("could not decode html: ")
                print(e)
            file.write("-------------------------------------------------------------------------------------------------------------------------\n")
            line_index = line_index + 2
    except Exception as e:
        print(e)
    finally:
        file.close()

    for post in posts:
        if post['user'] == u'DrorKFTC':
            print(post['title'])
            print(post['code'])
            print('---------------------------')
            print(post['content'])

