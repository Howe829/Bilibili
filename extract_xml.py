import xmltodict
import requests
import time
import redis
import json
from crc32Engine import Crc32Engine
from apscheduler.schedulers.blocking import BlockingScheduler

PROXY_POOL = 'http://106.13.58.203:5010/get'
astros = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']

class Aux:
    __slots__ = ['mid', 'uid', 'text', 'datetime']

    def __init__(self, mid, uid, text, datetime):
        self.mid = mid
        self.uid = uid
        self.text = text
        self.datetime = datetime

    def __str__(self):
        return '{} {} {} {}'.format(self.mid, self.text, self.uid, self.datetime)

    def to_dict(self):
        return {'_id': self.mid, 'text': self.text, 'uid': self.uid, 'datetime': self.datetime}


def timeStamp_2_formattime(ts):
    ta = time.localtime(ts)
    mytime = time.strftime('%Y-%m-%d %H:%M:%S', ta)
    return mytime


def get_proxy():
    head = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    return requests.get(PROXY_POOL, headers=head).json()


headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
headers['Host'] = 'comment.bilibili.com'
headers[
    'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Accept-Language'] = 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7'
headers['Connection'] = 'keep-alive'
headers['Upgrade-Insecure-Requests'] = '1'
headers['DNT'] = '1'
headers['Cache-Contro'] = 'max-age=0'
headers['If-Modified-Since'] = 'Mon, 15 Jun 2020 17:39:15 GMT'
cookie = {
    #        '_dfcaptcha':'2dd6f170a70dd9d39711013946907de0',
    'bili_jct': 'bili_jct5bbff2af91bd6d6c219d1fafa51ce179',
    'buvid3': '4136E3A9-5B93-47FD-ACB8-6681EB0EF439155803infoc',
    'CURRENT_FNVAL': '16',
    'DedeUserID': '293928856',
    'DedeUserID__ckMd5': '6dc937ced82650a6',
    'LIVE_BUVID': 'AUTO6915654009867897',
    #        'rpdid':'owolosliwxdossokkkoqw',
    'SESSDATA': '72b81477%2C1567992983%2Cbd6cb481',
    'sid': 'i2a1khkk',
    'stardustvideo': '1',
}

"""
更新本地弹幕池
"""


def update():
    s = requests.session()
    s.headers.update(headers)
    s.cookies.update(cookie)
    s.proxies.update({'http': 'http://{}'.format(get_proxy().get('proxy'))})
    print(s.proxies)
    crcEngine = Crc32Engine()
    res = s.get('http://comment.bilibili.com/70236628.xml')

    r = redis.StrictRedis(host='localhost', port=6379)
    my = xmltodict.parse(res.content.decode('utf-8'))
    for i in my['i']['d']:
        pl = i['@p'].split(',')
        datetime = timeStamp_2_formattime(int(pl[4]))
        mid = pl[-1]
        uid = crcEngine.crack(pl[-2])[0]
        a = Aux(mid, uid, i['#text'], datetime)
        if not r.sismember('mySet', mid) and i['#text'] in astros:
            print('Add    ', a)

            r.lpush('need_to_send', json.dumps(a.to_dict(), ensure_ascii=False))
            r.sadd('mySet', mid)
        else:
            print('Nothing Change')


if __name__ == '__main__':
    # scheduler = BlockingScheduler()
    # scheduler.add_job(update, 'interval', seconds=30)
    # scheduler.start()
    # print(get_proxy())
    update()