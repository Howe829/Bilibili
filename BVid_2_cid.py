import requests
import json


base_url = 'http://api.bilibili.com/x/web-interface/view?bvid={}'



def b_2_co(Bid):
    res = requests.get(base_url.format(Bid))
    js = json.loads(res.text)
    data = js.get('data')
    print(data['cid'])


b_2_co('BV19Q4y1A7Js')