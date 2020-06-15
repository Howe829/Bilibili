import xmltodict
import requests
import time
import redis
from crc32_crack import Crc32Engine
# #dom解析xml
# with open('test.xml') as f:
#
#      print(my['meeting'])

class Aux:
    __slots__ = ['mid', 'uid', 'text', 'datetime']

    def __init__(self, mid, uid, text, datetime):
        self.mid = mid
        self.uid = uid
        self.text = text
        self.datetime = datetime

    def __str__(self):
        return '{} {} {} {}'.format(self.mid, self.text, self.uid, self.datetime)


def timeStamp_2_formattime(ts):
    ta = time.localtime(ts)
    mytime = time.strftime('%Y-%m-%d %H:%M:%S', ta)
    return mytime


res = requests.get('http://comment.bilibili.com/197891020.xml')
crcEngine = Crc32Engine()

my = xmltodict.parse(res.content.decode('utf-8'))
for i in my['i']['d']:
    pl = i['@p'].split(',')
    datetime = timeStamp_2_formattime(int(pl[4]))
    mid = pl[-1]
    uid = crcEngine.crack(pl[-2])[0]
    a = Aux(mid, i['#text'], uid, datetime)
    print(a)
    time.sleep(1)
