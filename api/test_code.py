import json
import unittest
import warnings
import requests
from common.mysql import Mysql
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.s = SaveJson()
        # 获取登录ip
        cls.ip = r.get_ip()
        # 设置登录的类型
        cls.os = r.get_os()
        # 获取手机号
        cls.user = r.get_user()

    @unittest.skip('跳过')
    def test_01_get_code(self):
        """
        发送短信获取code
        """
        global code
        url = self.ip + '/api/v2/getVerificationCode'
        headers = {
            'os': self.os
        }
        data = {
            'mobile': self.user,
            'areaCode': '86'
        }
        r = requests.get(url, headers=headers, params=data)
        print()
        self.assertEqual(r.json()['msg'], '成功')
        # 查询数据库
        mysql = "select params from mesg_sms_send_record where mobile='18217484395' order by id DESC"
        results = Mysql().connect_mysql(mysql=mysql)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        # 获取短信验证码
        code = eval(results[0])['code']
        print("code:", code)

    @unittest.skip('跳过')
    def test_02_get_token(self):
        """
        短信登陆获取token
        """
        global headers
        url = self.ip + '/api/v2/vCodeLogin'
        data = {"mobile": "18217484395", "verificationCode": code, "areaCode": "86", "shareCode": ""}
        if self.os == '2':
            headers = {
                'os': self.os,
                'versionName': '1.6.11'
            }
        elif self.os == '1':
            headers = {
                'os': self.os
            }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        if r.json()['msg'] == '成功':
            print("短信登陆成功")
        token = r.json()['data']['token']
        # 将token写入配置文件
        ReadIni().write_ini(token)
        # 将用户信息写进json文件
        self.s.write_json('user', r.json()['data'])

    def test_03_pwdLogin(self):
        url = self.ip + '/api/v2/pwdLogin'
        headers = {
            "os": self.os,
            'versionName': '1.6.11'
        }
        data = {
            'username': '18217484395',
            'password': '123456'
        }
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        if r.json()['msg'] == '成功':
            print("密码登陆成功")
        token = r.json()['data']['token']
        # 将token写入配置文件
        ReadIni().write_ini(token)
        # 将用户信息写进json文件
        self.s.write_json('user', r.json()['data'])
