# -*- coding: utf-8 -*-
# author: ShenChao

import cookielib
import re
import urllib
import urllib2

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
    values = {}
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': user_agent,
        'Referer': 'www.zhihu.com',
        'Cookie:': 'q_c1=dd84cb409d78477397ecb6854fdc0e61|1458545532000|1458545532000; _xsrf=d8fb380226a9bc36517ce5be1424dc66; _za=3fd841ba-71cc-4bf0-a151-5fffa31ee643; cap_id="ZDYyNDg3MmIwNTA3NDdlYTg1YTUzODc4ODI3MThlYTk=|1458546206|f114e216ae5c8c29681c18d37a44708c808506d3"; __utmt=1; d_c0="ADAA2ugbpgmPTlSYf0ccVP-26FJ8nfRmSfY=|1458546210"; z_c0="QUJDSy1KdVhtZ2dYQUFBQVlRSlZUU1V6RjFkQS1Va01oekx2NTBnUmNSc3ZPT0dOc2N3MFFBPT0=|1458546213|cf7af4aa25311e0b55ef190e8c70dd6265f4abb8"; unlock_ticket="QUJDSy1KdVhtZ2dYQUFBQVlRSlZUUzJ0NzFhT1owWnFubXZBcHo2eDNwZkU1U0lZdnB3WVJ3PT0=|1458546213|ce1504f1fb92a6f7465522b5b1d29dcc03d13144"; n_c=1; __utma=51854390.1308926123.1458545535.1458545535.1458545535.1; __utmb=51854390.11.9.1458546286409; __utmc=51854390; __utmz=51854390.1458545535.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-2|2=registration_date=20150826=1^3=entry_date=20150826=1',
    }
    url = 'http://zhihu.com/question/'
    i = 0
    while True:
        i += 1
        try:
            request = urllib2.Request('%s%d'%(url,(i*5+4)), data, headers)
            # cookie = cookielib.CookieJar()
            # handler = urllib2.HTTPCookieProcessor(cookie)
            # opener = urllib2.build_opener(handler)
            response = urllib2.urlopen(request)
            plainHTML = response.read().decode('utf-8')
            print('the first question id is %d'%i)
            break
        except Exception, e:
            continue