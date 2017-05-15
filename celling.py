import requests
import json
from pprint import pprint
from datetime import datetime
import argparse
import time


URI = "http://www.lativ.com/Product/ProductInfo/"
MY_SIZE = 'M'
FMT = "%a, %d %b %Y %X GMT"
TIME_SLEEP_SEC = 5


def generate_modified_dt():
    now = datetime.now()
    return now.strftime(FMT)


header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.lativ.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'http://www.lativ.com/Detail/30407012',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'If-Modified-Since': generate_modified_dt()}


class RequestErr(Exception):
    def __init__(self, message):
        super(RequestErr, self).__init__(message)


class ProcessErr(Exception):
    def __init__(self, message):
        super(ProcessErr, self).__init__(message)


def get_info(_style_no):
    res = requests.get(URI, params={"styleNo": _style_no}, headers=header)
    if res.status_code == 200:
        res_json = res.json()
        res_json_info = json.loads(res_json['info'])
        return res_json_info
    else:
        pprint(res.content)
        pprint(res.status_code)
        raise RequestErr('no 200 return')
    # item_list = res_json_info['ItemList']
    # return res_json_info


def process_data(info_list):
    """
    return 
    {
        "浅蓝": {"invet": 1},
        "蓝色": {"invet": 14}

    }
    """
    target = {}
    for info in info_list:
        for item in info['ItemList']:
            if item['size'] == MY_SIZE:
                target[info['color']] = {
                    "itemNo": item['sn'],
                    "invt": item['invt']
                }
            else:
                continue
    pprint(target)
    for rst in target.values():
        if rst['invt'] > 0:
            raise ProcessErr('Got it !')
    return target


def parse_product_no():
    parser = argparse.ArgumentParser(description='lativ args')
    parser.add_argument('product_no', type=int,
                        help='lativ product number')

    args = parser.parse_args()
    p_no = args.product_no
    if p_no > 10000:
        return int(p_no / 1000)
    else:
        return p_no

    # print(args.accumulate(args.integers))


if __name__ == "__main__":
    _p_no = parse_product_no()
    while True:
        try:
            _info_list = get_info(_p_no)
            _data = process_data(_info_list)
        except RequestErr as e:
            time.sleep(TIME_SLEEP_SEC)
        except ProcessErr as e:
            print("!!!!!!!!")
            break
        else:
            print('--' * 10)
            print('\n')
            time.sleep(TIME_SLEEP_SEC)
