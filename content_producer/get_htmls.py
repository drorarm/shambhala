import requests
from reader import read_response
from db_writer_mysql import write_posts_to_db

# http://old.tapuz.co.il/communa/userCommunaMsges.asp?CommunaId=40780&firstmsg=1
cookies_arr = "__utmz=136157492.1574063410.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=6e86a43745a9e2f0:T=1574063397:S=ALNI_MZAbiHeFTqIqH7oySt3k1Nrn6gkag; _fbp=fb.2.1574063410622.1377423214; Tapuz%5Fsign=signName=; Tapuz%5FForums=UserId=3998854&UserName=DrorKFTC&nick=&UserEmail=droram%40gmail.com&enc=351532&ds=2d4772bc5d2f97a81ad9d2d60638d786&sex=1&age=34&areaId=1&areaDesc=Center&signName=; TLiveUser=656k210QQgp2RVoUDuUsmZRNb45ZAf4QLm70MYdrU6fNul7dqC4trIHlANvxFiYtLZqcGiPU+4tHZfn2fc4tYX+4YR4iVRl9q2poha8WZYw=; notifyMail=1; notifyLms=0; _ga=GA1.3.1274179139.1574063410; _omappvp=cqG4ypqQvjzR5JzAeqmGLG7y8SrnAFWY8PVBwc9MgONBFNbXO4t1ETZ8uquW0McIbXz3dMSPtL5I1T4oijLvgDYBEi7r2ReY; trc_cookie_storage=taboola%2520global%253Auser-id%3Dca78d5bc-c290-461e-8c5f-66d97ad3560e-tuct4bd8a2a; __qca=P0-420307124-1575396141971; __adroll_fpc=1dc4ad279aae947145860173ca32b2e4-s2-1575396151378; __ar_v4=3AM6BLBU3ZDKDLIR2L4KTE%3A20200002%3A89%7CPYW3ZG2MLJFLVOVRMJ2JMN%3A20200002%3A89%7C6COZHMN4P5AY7IPTOJ4SGI%3A20200002%3A89; _cb_ls=1; _cb=BZPLxsDMrGbmB8aiWc; __utmc=136157492; ASPSESSIONIDSSACBTBR=MONDMHLAACMEDCDFIIKMIKCB; PopTapuzonC=40780; ASPSESSIONIDCACTRTBR=FKPHMHLADEECFACDFCNHDCIJ; ASP.NET_SessionId=dqxqpqyvjgt1kq45yerr5b45; ASPSESSIONIDAQBTDDBR=JHJNDLDBJMOHLEMDPOPOPNIE; _gid=GA1.3.2071484443.1586692720; _chartbeat2=.1584215037457.1586692721047.0000000000000111.BX2HQ1DpHTwYBxpjuTBDMjNfDHkLGw.1; ASPSESSIONIDAQCTADAQ=FFHEJNDBNAOJLECIIDLPACII; __utma=136157492.1274179139.1574063410.1586504268.1586692727.52; communa%5Fmaavaron=shown; TapuzConnun=; TapuzCommun=Commun40780=yes; TS01ab3eda=01d8d2b3e55d35b8a22d3fc31163cb2140aab33064da83c361ca3885d45be01ed6279d34894041bb4eb27448a566b574552320342dfaa5a84557c12d59b2f4c219ce8f368c04f752ee5bfe8f1cb7fb3c28ad745a706243cb8f9dec4b6ddc9eaa7d20d088f8; ASPSESSIONIDAQDRDAAS=GBPOEKMAGMCFHKKPBBFIENCJ; ASPSESSIONIDCSDTCDBQ=DFABOIDBHDEOHBCKNHLOLCCL; TS013e48fe=01d8d2b3e5baea0ef79b595d6e2eb95b35fa11f50ebe2938be4ba000f02379edd9f94592f98d9e41bc3a754cc0aac4fd929e82ea3a7ad24c86cefdd5c499ea8993d486d07a0894488a0dd13a1e2987c205d8069944c2d4e99784cdad4f3291b34666861f9aceadd75a95a2ac9849a1ddd5a3fdabd637b4eea8bbddbfbe01e28fe443d9c97f7b248385b3473d454802d6118f32619b; __utmb=136157492.14.10.1586692727".split(';')

cookies = dict()
for cookie in cookies_arr:
    result = cookie.strip(' ').partition('=')
    cookies[result[0]] = result[2]

headers = dict()
headers['Host'] = 'old.tapuz.co.il'
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Accept-Language']= 'en-US,en;q=0.9,he;q=0.8'
msg_offset = 0
response = requests.get(f'http://old.tapuz.co.il/communa/userCommunaMsges.asp?CommunaId=40780&firstmsg={msg_offset}',
                        headers=headers, cookies=cookies)

while response.status_code == 200:
    page_posts = read_response(response.text)
    print(f'finish reading page {int(msg_offset/15+1)}')
    write_posts_to_db(page_posts)

    print(f'finish Update DB in page {int(msg_offset/15+1)}')

    msg_offset = msg_offset + 15
    response = requests.get(f'http://old.tapuz.co.il/communa/userCommunaMsges.asp?CommunaId=40780&firstmsg={msg_offset}',
                        headers=headers, cookies=cookies)

if response.status_code != 200:
    print(f'the request return {response.status_code} due to {response.reason} when msg offset is {msg_offset}')


'''
curl 'http://old.tapuz.co.il/communa/userCommunaMsges.asp?CommunaId=40780&firstmsg=1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'Referer: http://old.tapuz.co.il/communa/userCommunaMsges.asp?CommunaId=40780&firstmsg=1' -H 'Accept-Language: en-US,en;q=0.9,he;q=0.8' -H 'Cookie: __utmz=136157492.1574063410.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=6e86a43745a9e2f0:T=1574063397:S=ALNI_MZAbiHeFTqIqH7oySt3k1Nrn6gkag; _fbp=fb.2.1574063410622.1377423214; Tapuz%5Fsign=signName=; Tapuz%5FForums=UserId=3998854&UserName=DrorKFTC&nick=&UserEmail=droram%40gmail.com&enc=351532&ds=2d4772bc5d2f97a81ad9d2d60638d786&sex=1&age=34&areaId=1&areaDesc=Center&signName=; TLiveUser=656k210QQgp2RVoUDuUsmZRNb45ZAf4QLm70MYdrU6fNul7dqC4trIHlANvxFiYtLZqcGiPU+4tHZfn2fc4tYX+4YR4iVRl9q2poha8WZYw=; notifyMail=1; notifyLms=0; _ga=GA1.3.1274179139.1574063410; _omappvp=cqG4ypqQvjzR5JzAeqmGLG7y8SrnAFWY8PVBwc9MgONBFNbXO4t1ETZ8uquW0McIbXz3dMSPtL5I1T4oijLvgDYBEi7r2ReY; trc_cookie_storage=taboola%2520global%253Auser-id%3Dca78d5bc-c290-461e-8c5f-66d97ad3560e-tuct4bd8a2a; __qca=P0-420307124-1575396141971; __adroll_fpc=1dc4ad279aae947145860173ca32b2e4-s2-1575396151378; __ar_v4=3AM6BLBU3ZDKDLIR2L4KTE%3A20200002%3A89%7CPYW3ZG2MLJFLVOVRMJ2JMN%3A20200002%3A89%7C6COZHMN4P5AY7IPTOJ4SGI%3A20200002%3A89; _cb_ls=1; _cb=BZPLxsDMrGbmB8aiWc; __utmc=136157492; ASPSESSIONIDSSACBTBR=MONDMHLAACMEDCDFIIKMIKCB; PopTapuzonC=40780; ASPSESSIONIDCACTRTBR=FKPHMHLADEECFACDFCNHDCIJ; ASP.NET_SessionId=dqxqpqyvjgt1kq45yerr5b45; ASPSESSIONIDAQBTDDBR=JHJNDLDBJMOHLEMDPOPOPNIE; _gid=GA1.3.2071484443.1586692720; _chartbeat2=.1584215037457.1586692721047.0000000000000111.BX2HQ1DpHTwYBxpjuTBDMjNfDHkLGw.1; ASPSESSIONIDAQCTADAQ=FFHEJNDBNAOJLECIIDLPACII; __utma=136157492.1274179139.1574063410.1586504268.1586692727.52; communa%5Fmaavaron=shown; TapuzConnun=; TapuzCommun=Commun40780=yes; TS01ab3eda=01d8d2b3e55d35b8a22d3fc31163cb2140aab33064da83c361ca3885d45be01ed6279d34894041bb4eb27448a566b574552320342dfaa5a84557c12d59b2f4c219ce8f368c04f752ee5bfe8f1cb7fb3c28ad745a706243cb8f9dec4b6ddc9eaa7d20d088f8; ASPSESSIONIDAQDRDAAS=GBPOEKMAGMCFHKKPBBFIENCJ; ASPSESSIONIDCSDTCDBQ=DFABOIDBHDEOHBCKNHLOLCCL; TS013e48fe=01d8d2b3e5baea0ef79b595d6e2eb95b35fa11f50ebe2938be4ba000f02379edd9f94592f98d9e41bc3a754cc0aac4fd929e82ea3a7ad24c86cefdd5c499ea8993d486d07a0894488a0dd13a1e2987c205d8069944c2d4e99784cdad4f3291b34666861f9aceadd75a95a2ac9849a1ddd5a3fdabd637b4eea8bbddbfbe01e28fe443d9c97f7b248385b3473d454802d6118f32619b; __utmb=136157492.14.10.1586692727' --compressed --insecure


GET /communa/userCommunaMsges.asp?CommunaId=40780&firstmsg=1 HTTP/1.1
Host: old.tapuz.co.il
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://old.tapuz.co.il/communa/userCommunaMsges.asp?CommunaId=40780&firstmsg=1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,he;q=0.8
Cookie: __utmz=136157492.1574063410.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=6e86a43745a9e2f0:T=1574063397:S=ALNI_MZAbiHeFTqIqH7oySt3k1Nrn6gkag; _fbp=fb.2.1574063410622.1377423214; Tapuz%5Fsign=signName=; Tapuz%5FForums=UserId=3998854&UserName=DrorKFTC&nick=&UserEmail=droram%40gmail.com&enc=351532&ds=2d4772bc5d2f97a81ad9d2d60638d786&sex=1&age=34&areaId=1&areaDesc=Center&signName=; TLiveUser=656k210QQgp2RVoUDuUsmZRNb45ZAf4QLm70MYdrU6fNul7dqC4trIHlANvxFiYtLZqcGiPU+4tHZfn2fc4tYX+4YR4iVRl9q2poha8WZYw=; notifyMail=1; notifyLms=0; _ga=GA1.3.1274179139.1574063410; _omappvp=cqG4ypqQvjzR5JzAeqmGLG7y8SrnAFWY8PVBwc9MgONBFNbXO4t1ETZ8uquW0McIbXz3dMSPtL5I1T4oijLvgDYBEi7r2ReY; trc_cookie_storage=taboola%2520global%253Auser-id%3Dca78d5bc-c290-461e-8c5f-66d97ad3560e-tuct4bd8a2a; __qca=P0-420307124-1575396141971; __adroll_fpc=1dc4ad279aae947145860173ca32b2e4-s2-1575396151378; __ar_v4=3AM6BLBU3ZDKDLIR2L4KTE%3A20200002%3A89%7CPYW3ZG2MLJFLVOVRMJ2JMN%3A20200002%3A89%7C6COZHMN4P5AY7IPTOJ4SGI%3A20200002%3A89; _cb_ls=1; _cb=BZPLxsDMrGbmB8aiWc; __utmc=136157492; ASPSESSIONIDSSACBTBR=MONDMHLAACMEDCDFIIKMIKCB; PopTapuzonC=40780; ASPSESSIONIDCACTRTBR=FKPHMHLADEECFACDFCNHDCIJ; ASP.NET_SessionId=dqxqpqyvjgt1kq45yerr5b45; ASPSESSIONIDAQBTDDBR=JHJNDLDBJMOHLEMDPOPOPNIE; _gid=GA1.3.2071484443.1586692720; _chartbeat2=.1584215037457.1586692721047.0000000000000111.BX2HQ1DpHTwYBxpjuTBDMjNfDHkLGw.1; ASPSESSIONIDAQCTADAQ=FFHEJNDBNAOJLECIIDLPACII; __utma=136157492.1274179139.1574063410.1586504268.1586692727.52; communa%5Fmaavaron=shown; TapuzConnun=; TapuzCommun=Commun40780=yes; TS01ab3eda=01d8d2b3e55d35b8a22d3fc31163cb2140aab33064da83c361ca3885d45be01ed6279d34894041bb4eb27448a566b574552320342dfaa5a84557c12d59b2f4c219ce8f368c04f752ee5bfe8f1cb7fb3c28ad745a706243cb8f9dec4b6ddc9eaa7d20d088f8; ASPSESSIONIDAQDRDAAS=GBPOEKMAGMCFHKKPBBFIENCJ; ASPSESSIONIDCSDTCDBQ=DFABOIDBHDEOHBCKNHLOLCCL; TS013e48fe=01d8d2b3e5baea0ef79b595d6e2eb95b35fa11f50ebe2938be4ba000f02379edd9f94592f98d9e41bc3a754cc0aac4fd929e82ea3a7ad24c86cefdd5c499ea8993d486d07a0894488a0dd13a1e2987c205d8069944c2d4e99784cdad4f3291b34666861f9aceadd75a95a2ac9849a1ddd5a3fdabd637b4eea8bbddbfbe01e28fe443d9c97f7b248385b3473d454802d6118f32619b; __utmb=136157492.14.10.1586692727

'''
