# -*- coding: utf-8 -*-
# author: ShenChao

import cookielib
import re
import urllib
import urllib2
import threadPool
from multiprocessing import Pool, Process
import time
import os
import requests

def get_zhihu_min_qid(i, *args, **kwargs):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
    values = {}
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': user_agent,
        'Referer': 'www.zhihu.com',
        # 'Cookie:': '_za=43d95061-7c27-49f5-83d1-e39475d8c69f; _xsrf=62052201602318af3d8a5836b3b4fc6e; udid="ADAAwFgDlQmPTp-FsLaaq7ZsGB8_XF_dzu8=|1457502030"; d_c0="AECAB23ioQmPTgK689KjKJHccj1h9L4P-Hs=|1458262705"; cap_id="ZTc0YmU0MWEyM2RhNDU1NWJmOWJmYjU2MGMwYzQyMzg=|1458287762|30d0791d11e737d4f2b277fbafc59d6da0120aca"; z_c0="QUFCQXVzWWNBQUFYQUFBQVlRSlZUWmRCRTFjbDF5YUk1LVpEN0lRRnFMekVFbmtxWjRrcXZnPT0=|1458287767|551c5d728d385cd734144567e781ef42faa15ac9"; q_c1=7d096660be42428f81d2495690cabeab|1458781139000|1445221549000; __utmt=1; __utma=51854390.37124741.1458810574.1458869191.1458872304.3; __utmb=51854390.3.9.1458874466876; __utmc=51854390; __utmz=51854390.1458705672.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20130801=1^3=entry_date=20130801=1',
    }
    url = 'http://zhihu.com/question/'
    while True:
        i += 1
        try:
            # if i%1000 == 0:
            #     print('task_seq %d: current id is %d\n'%(kwargs['task_seq'], i*kwargs['task_total']+kwargs['task_seq']))
            request = urllib2.Request('%s%d'%(url,(i*kwargs['task_total']+kwargs['task_seq'])), data, headers)
            response = urllib2.urlopen(request)
            plainHTML = response.read().decode('utf-8')
            print('the first question id is %d'%(i*kwargs['task_total']+kwargs['task_seq']))
            f = open('./zhihu_min_qid', 'a')
            f.write('the first question id is %d\n'%(i*kwargs['task_total']+kwargs['task_seq']))
            f.flush()
            f.close()
            break
        except Exception, e:
            continue
    return False


def runThreadTask(i):
    pool = threadPool.ThreadPool()
    pool.startTask(get_zhihu_min_qid, workers=400, func_args=(i,))
    print('%d %s'%(os.getpid(),'all started'))
    while True:
        time.sleep(10)


def get_url_content(url):
    res = requests.get(url)
    # print(res.json())
    return res.json()


def test(i):
    f = open('./zhihu_min_qid', 'a')
    f.writelines('123')
    f.flush()
    f.close()
    print i*i

if __name__ == '__main__':
    # print(os.getpid())
    # pool = Pool(processes=8)
    # pool.map(runThreadTask, range(0, 50000, 6250))
    # get_zhihu_min_qid(41483147, task_total=1,task_seq=0)
    jobj = get_url_content('http://ip.taobao.com/service/getIpInfo.php?ip=117.89.90.102')
    print(jobj['data']['city'] == u'南京市')
    print(jobj['data']['region'] == u'江苏省')

{
    u'code': 0, 
    u'data': {
        u'ip': u'117.89.90.102', 
        u'city': u'\u5357\u4eac\u5e02', 
        u'area_id': u'300000', 
        u'region_id': u'320000', 
        u'area': u'\u534e\u4e1c', 
        u'city_id': u'320100', 
        u'country': u'\u4e2d\u56fd', 
        u'region': u'\u6c5f\u82cf\u7701', 
        u'isp': u'\u7535\u4fe1', 
        u'country_id': u'CN', 
        u'county': u'', 
        u'isp_id': 
        u'100017', 
        u'county_id': u'-1'
    }
}