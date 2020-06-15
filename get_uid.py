import json
from config import sess, csrf
CSRF = 'd4500802543b87cef85836fe16fb996e'
SBDF = 'f793f45433685adab996fb4b2b10d630'
HEADERS = {'Accept': '*/*',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'DNT': '1',
           'Origin': 'https://www.bilibili.com',
           'Referer': 'https://www.bilibili.com/video/BV1a54y1Q7Wc',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
           }

ADD_URL = 'https://api.bilibili.com/x/dm/filter/user/add'
DEL_URL = 'https://api.bilibili.com/x/dm/filter/user/del'


def Del(uid):
    DEL_DATA = {'ids': uid, 'jsonp': 'jsonp', 'csrf': csrf}
    res = sess.post(DEL_URL, data=DEL_DATA, headers=HEADERS)
    if res.status_code == 200:
        print(res.text)
    else:
        print('Del Failed:', res.status_code)


def Add(filter: str):
    ADD_DATA = {'type': 2, 'filter': filter, 'jsonp': 'jsonp', 'csrf': csrf}

    res = sess.post(ADD_URL, data=ADD_DATA, headers=HEADERS)
    if res.status_code == 200:
        print(res.text)
        js = json.loads(res.text)
        ids = ''
        if js.get('code') == 0:
            ids = js['data']['id']
            Del(ids)
        return ids
    else:
        print('Add Failed:', res.status_code)

    return ''


if __name__ == '__main__':
    print(Add('2cfa248a'))