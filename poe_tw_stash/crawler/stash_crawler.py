# -*- coding: utf-8 -*-
# author: ShenChao

from collections import deque
from threading import Thread, Lock
import datetime
import django
import json
import logging
import os
import requests
import sys
import time
import uuid
reload(sys)
sys.setdefaultencoding("utf-8")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poe_tw_stash.settings")
if django.VERSION >= (1, 7):
    django.setup()
from crawler.models import *
from django.db.utils import OperationalError
from django.core.cache import cache

BASE_URL = 'http://web.poe.garena.tw/api/public-stash-tabs'
NEXT_URL = BASE_URL + '/?id=%s'

STATE_STOP = 0
STATE_RUN = 1
request_worker_count = 0
request_worker_count_lock = Lock()
container = deque()


class RequestWorker(Thread):

    def __init__(self, startnew=False):
        super(RequestWorker, self).__init__()
        self.state = STATE_STOP
        if startnew:
            self.first_next_id = '4431201-4506673-4532501'
        else:
            self.first_next_id = cache.get('poe_tw_stash_next_id')
            if not self.first_next_id:
                # start of essence league
                self.first_next_id = '4431201-4506673-4532501'
                # self.first_next_id = '5249772-5291470-5323025'
        self.next_id = self.first_next_id
        

    def stop(self):
        self.state = STATE_STOP

    def run(self):
        self.state = STATE_RUN
        global container
        global request_worker_count
        global request_worker_count_lock
        while self.state == STATE_RUN:
            res = requests.get(NEXT_URL % self.next_id).json()
            next_change_id = res.get('next_change_id', self.first_next_id)
            if not next_change_id or next_change_id == self.first_next_id:
                logging.info('no new stashes')
                request_worker_count_lock.acquire()
                request_worker_count -= 1
                request_worker_count_lock.release()
                break
            self.next_id = next_change_id
            logging.info('next query id: %s' % next_change_id)
            print('next query id: %s' % next_change_id)
            cache.set('poe_tw_stash_next_id', self.next_id)
            container.append(res.get('stashes', {}))


class RequestWorkerManager(Thread):

    def __init__(self, startnew=False):
        super(RequestWorkerManager, self).__init__()
        self.last_create_time = 0
        self.startnew = startnew

    def run(self):
        global request_worker_count
        global request_worker_count_lock
        request_worker = RequestWorker()
        request_worker.start()
        self.last_create_time = time.time()
        request_worker_count_lock.acquire()
        request_worker_count = 1
        request_worker_count_lock.release()
        while True:
            # 10mins
            if request_worker_count < 1 and (time.time() - self.last_create_time > 600):
                request_worker = RequestWorker(startnew=True)
                request_worker.start()
                self.last_create_time = time.time()
                request_worker_count_lock.acquire()
                request_worker_count += 1
                request_worker_count_lock.release()
                logging.info('current request worker count: %d' %
                             request_worker_count)
                print('current request worker count: %d' %
                      request_worker_count)
            else:
                time.sleep(10)


class ProcessWorker(Thread):

    def __init__(self):
        super(ProcessWorker, self).__init__()
        self.state = STATE_STOP

    def stop(self):
        self.state = STATE_STOP

    def run(self):
        self.state = STATE_RUN
        global container
        while self.state == STATE_RUN:
            try:
                stashes = container.popleft()
                logging.info(
                    'processing stashes, current stashes length: %d' % len(stashes))
                print('processing stashes, current stashes length: %d' %
                      len(stashes))

                item_list = []
                for stash in stashes:
                    items = stash.get('items', '')  # list
                    stashType = stash.get('stashType', '')  # str
                    stash_tag = stash.get('stash', '')  # str
                    accountName = stash.get('accountName', '') or ''  # str
                    public = stash.get('public', '')  # boolean
                    lastCharacterName = stash.get(
                        'lastCharacterName', '')  # str
                    id = stash.get('id', '')  # str
                    stash, created = Stash.objects.get_or_create(id=id)
                    stash.stashType = stashType
                    stash.stash = stash_tag
                    stash.accountName = accountName
                    stash.public = public
                    stash.lastCharacterName = lastCharacterName
                    stash.save()
                    for item in items:
                        if item['league'] == u'精髓聯盟':  # ESC
                            storeItem, created = BasicItem.objects.get_or_create(id=item['id'])
                            for k, v in item.items():
                                try:
                                    if k == 'league':
                                        storeItem.league = BasicItem.toleague(v)
                                    else:
                                        setattr(storeItem, k, self.toStoreType(v))
                                except Exception, e:
                                    logging.exception(e)
                            storeItem.save()
                            item_list.append(storeItem)
                if item_list != []:
                    stash.items.clear()
                    stash.items.add(*item_list)

            except IndexError, e:
                time.sleep(0.1)

            except OperationalError, e:
                django.db.close_old_connections()

            except Exception, e:
                logging.exception(e)


    def toStoreType(self, v):
        if type(v) == type([]) or type(v) == type({}):
            return json.dumps(v, ensure_ascii=False).encode('utf-8')
        return v

if __name__ == '__main__':
    request_manager = RequestWorkerManager(startnew=False)
    request_manager.start()
    for i in range(4):
        process_worker = ProcessWorker()
        process_worker.start()

 #    {u'socketedItems': [],
 # u'corrupted': False,
 # u'typeLine': u'瓦爾寶珠',
 # u'talismanTier': 4,
 # u'implicitMods': [u'增加 20% 敵人暈眩時間'],
 # u'flavourText': [u'「對我們凡人來說，時間稍縱即逝；\r',
 # u'我只是試著平衡罷了。」\r',
 # u'- 女王首席預言者多里亞尼'],

 # u'id': u'8dd44cd44e9d86f96ecfafc1ffd97d212da66dc412010b37c65ea0210c09526c',
 # u'lockedToCharacter': False,
 # u'verified': False,
 # u'craftedMods': [u'+25 敏捷'],
 # u'support': True,
 # u'secDescrText': u'迅速穿越敵人並同時造成武器傷害。限定匕首、爪以及單手劍。',
 # u'sockets': [],
 # u'note': u'~price 11111111 exa',
 # u'duplicated': True,
 # u'frameType': 5,
 # u'explicitMods': [u'腐化一件裝備並隨機修改其能力'],
 # u'nextLevelRequirements': [{u'displayMode': 0, u'values': [[u'51',0]], u'name': u'等級'},
 #                           {u'displayMode': 1, u'values': [[u'115',0]], u'name': u'智慧'}],
 # u'additionalProperties': [{u'displayMode': 2, u'values': [[u'1 / 3231',0]],
 #                            u'name': u'經驗值',
 #                            u'progress': 0.000309501716401}],
 # u'descrText': u'右鍵點擊此物品，再左鍵點擊一件物品來使其腐化。請注意，腐化過的物品無法再使用通貨改變其屬性。\n按住 Shift 點擊以分開堆疊',
 # u'inventoryId': u'Stash1',
 # u'requirements': [{u'displayMode': 0,
 #                    u'values': [[u'8',0]],
 #                    u'name': u'等級'},
 #                    {u'displayMode': 1,
 #                     u'values': [[u'18',0]], u'name': u'敏捷'}],
 # u'properties': [{u'displayMode': 0,
 #                  u'values': [[u'10 / 10',0]],
 #                  u'name': u'堆疊數量'}],
 # u'icon': u'http://tw.webcdn.pathofexile.com/image/Art/2DItems/Currency/CurrencyVaal.png?scale=1&stackSize=10&w=1&h=1&v=64114709d67069cd665f8f1a918cd12a3',
 # u'league': u'標準模式',
 # u'cosmeticMods': [u'使用 <<set:MS>><<set:M>><<set:S>>莫考之擁 造型'],
 # u'artFilename': u'TheGambler',
 # u'name': u'',
 # u'enchantMods': [u'被擊中時在攻擊時附加怨恨之誓'],
 # u'h': 1,
 # u'identified': True,
 # u'ilvl': 0,
 # u'w': 1,
 # u'y': 2,
 # u'x': 2}
