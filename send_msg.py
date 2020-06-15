from Login import login
import time
import json
from apscheduler.schedulers.blocking import BlockingScheduler
astros = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']

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
        'msg[sender_uid]': '106592867',
        'msg[receiver_id]': str(id),
        'msg[receiver_type]': '1',
        'msg[msg_type]': '1',
        'msg[msg_status]': '0',
        'msg[content]': json.dumps({'content': msg}, ensure_ascii=False),
        'msg[timestamp]': int(time.time()),
        'msg[dev_id]': '',
        'build': '0',
        'mobi_app': 'web',
        'csrf_token': csrf

    }
    res = sess.post(headers=headers, url=url, data=data, timeout=10)
    if res.status_code == 200:
        print('发送成功！', res.text,id)
    else:
        print('发送失败', res.status_code)


def message_handler():
    import redis

    myRedis = redis.StrictRedis('localhost', port=6379)

    r = myRedis.rpop(name='need_to_send')
    while r:
        danmu = r.decode('utf-8')
        dmd = json.loads(danmu)
        uid = dmd['uid']
        astro = dmd['text']
        if astro in astros:
            msg = myRedis.get(astro)
            if msg:
                msg_send(uid, msg.decode('utf-8'))
            r = myRedis.rpop(name='need_to_send')


if __name__ == '__main__':
   message_handler()
   scheduler = BlockingScheduler()
   scheduler.add_job(message_handler, 'interval', seconds=30)
   scheduler.start()