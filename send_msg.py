from Login import login
import time

url = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'

headers = {'Accept': 'application/json, text/plain, */*',
           'Content-Type': 'application/x-www-form-urlencoded',
           'DNT': '1',
           'Origin': 'https://message.bilibili.com',
           'Referer': 'https://message.bilibili.com/',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

sess, csrf = login()


def msg_send(id, msg: str):
    data = {
        'msg[sender_uid]': 106592867,
        'msg[receiver_id]': id,
        'msg[receiver_type]': 1,
        'msg[msg_type]': 1,
        'msg[msg_status]': 0,
        'msg[content]': {'content': msg},
        'msg[timestamp]': int(time.time()),
        'msg[dev_id]': '',
        'build': 0,
        'mobi_app': 'web',
        'csrf_token': csrf

    }
    res = sess.post(headers=headers, url=url, data=data)
    if res.status_code == 200:
        print('发送成功！', res.text)
    else:
        print('发送失败', res.status_code)


if __name__ == '__main__':
    msg_send(109097115, 'this is sent by python.')
