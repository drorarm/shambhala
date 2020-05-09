import re
from reader import decode_mtbl
import html2text
from datetime import datetime



a = """מקדש הקונג פו - 5.4.2020 עד 11.4.20
![\"|פיה|\"](\"http://www.timg.co.il/tapuzForum/images/Emo230.gif\")

"""

print(a.find('!['))

# [1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]
#x = re.search(r'[1-9]|1[0-9]|2[0-9]|3[0-1]\.', a)

date_regex = r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-)([1-9]|1[0-2])(\.|-)(20)?(1[6-9]|2[0-9])'
x = re.findall(date_regex, a)
y = re.search(r'([1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-)([1-9]|1[0-2])(\.|-)(20)?(1[6-9]|2[0-9])', a)

#date_str = y.group(0)
first_date_str = ''.join(x[0])
year_len = len(first_date_str) - first_date_str.rfind('.') - 1

s = datetime.strptime(first_date_str, f"%d.%m.%{'Y' if year_len == 4 else 'y' }")
print(s)
b = "fhghjkdgfakjhfg"
z = re.findall(date_regex, b)

print(len(z))




# a = 'MTbl(0,4,88,57553784,"-",61,"משיעורי השבוע שלי",1797851,0,"0","0","20:59","26/02/20","בהתחלה");'
#
# print(a.split(','))
#
#
#htmler = html2text.HTML2Text()
#print(decode_mtbl(a, htmler))
# print(a.encode(encoding='cp1255').decode(encoding='cp1255'))
#
#
# mtbl_args = a[5:-3].split(',')
#
# user = mtbl_args[-1].strip('\"')
# print(f'args : {mtbl_args} ; user : {user}')

# inputString = 'dfksjdhf "hello" dfhdkfh '
# code = re.findall(r'"([^"]*)"', inputString)
# print code
