import json
import unittest
from pprint import pprint

import requests


def outPut(url, data, r):
    return "'\033[1;31;40m请求\033[0m'：{} \n'\033[1;31;40m数据\033[0m':{} \n'\033[1;31;40m返回\033[0m'：{} ".format(url, data, r.json())


url = 'https://pre.mars-tech.com.cn/api/Login'
headers = {
    'os': '0'
}
data = {
    'username': '18217484395',
    'password': '123456'
}

r = requests.post(url, headers=headers, data=json.dumps(data))
pprint(r.json())
print(outPut(url, data, r))


