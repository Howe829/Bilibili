from qrcode_gen import generate
import requests
import json
import time
import webbrowser


def get_login_url():
    url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
    res = requests.get(url)
    if res.status_code == 200:
        js = json.loads(res.text)
        if js.get('code') == 0:
            login_url = js['data']['url']
            oauthKey = js['data']['oauthKey']
            name = generate(login_url)
            webbrowser.open('http://localhost:5000/loginqr/{}'.format(name))
            return oauthKey
    return ''


def login():
    HEADERS = {'Accept': '*/*',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'DNT': '1',
               'Origin': 'https://www.bilibili.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
               }
    url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
    oauthKey = get_login_url()
    print('oKey', oauthKey)
    csrf = ''
    data = {'oauthKey': oauthKey, 'gourl': 'www.bilibili.com'}
    with requests.session() as sess:
        while True:
            res = sess.post(url, data=data, headers=HEADERS)
            if res.status_code == 200:
                print('请扫描二维码以登录Bilibili.com')
                js = json.loads(res.text)
                print(js)
                if js.get('data') == -5:
                    print('扫码成功！请确认登录。')
                if js.get('status') == True:
                    lodata = sess.get('http://api.bilibili.com/nav', headers=HEADERS)

                    if lodata.status_code == 200:
                        ljs = json.loads(lodata.text)
                        if ljs.get('code') == 0:
                            ldata = ljs['data']
                            if ldata['isLogin']:
                                print('登录成功！')
                                csrf = sess.cookies.get_dict()['bili_jct']
                                break
                time.sleep(10)

    return sess, csrf


if __name__ == '__main__':
    login()
