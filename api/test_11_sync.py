import datetime
import time
import unittest
import warnings
import requests
import json
from parameterized import parameterized
from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


@unittest.skip('跳过')
class TestLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.s = SaveJson()
        # 获取环境
        cls.ip = r.get_ip()
        # 设置任务类型
        cls.taskType = '2'
        # 设置登录的类型
        cls.os = r.get_os()
        # 获取token
        cls.token = r.get_token()
        # 设置请求头
        cls.headers = {
            'os': cls.os,
            'Authorization': cls.token,
            'versionName': '1.6.11'
        }

    @classmethod
    def tearDownClass(cls) -> None:
        """
        从数据库中删除任务
        """

    @staticmethod
    def outPut(url, data=None, r=None):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    def test_01_get_user_company(self):
        """
        获取当前用户所有关联企业
        """
        url = self.ip + '/api/company/listBindCompany'
        headers = self.headers
        r = requests.get(url, headers=headers)
        print(self.outPut(url, r=r))
        self.assertEqual(r.json()['msg'], '成功')
        self.s.write_json('company', r.json()['data'])

    def test_02_assert_company(self):
        """
        判断当前用户是否在春安测试下，如果不是则切换到春安测试
        """
        global id
        companyInfo = self.s.read_json('company')
        userInfo = self.s.read_json('user')  # 获取
        if userInfo['companyName'] != '春安测试':
            print('--当前用户在{}下，需要切换到春安测试企业--'.format(userInfo['companyName']))
            companies = []
            for company in companyInfo:
                companies.append(company['name'])
                if company['name'] == '春安测试':
                    id = company['id']
            if "春安测试" not in companies:
                print('您尚未加入春安测试企业，若外理同步请联系相关人员将您拉到该公司下')
            else:
                # 切换到春安测试企业
                url = self.ip + '/api/user/v2/switchBody'
                headers = self.headers
                data = {
                    'companyId': str(id)
                }
                r = requests.get(url, headers=headers, params=data)
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
                print("切换到春安测试企业成功")
        elif userInfo['companyName'] == '春安测试':
            print('--当前用户在{}下，用例继续执行--'.format(userInfo['companyName']))

    @parameterized.expand([('OCEAN TRADE', 'V2427', 'Shanghai Port', '军工路码头', '任务描述', '顾鹏')])
    def test_03_add_task(self, vesselName, voyage, portName, terminalName, description, customer):
        """
        添加任务并将任务信息写入文件
        """
        global taskName

        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        threeDayAgo = (datetime.datetime.now() + datetime.timedelta(days=7))
        # 获取7天后的时间戳
        timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        a = '000'
        url = self.ip + '/task/index/addTask'
        headers = self.headers
        if self.os == '1':
            taskName = '安卓/监装/同步外理数据'
        elif self.os == '2':
            taskName = 'IOS/监装/同步外理数据'
        data = {"taskName": taskName, "taskType": self.taskType, "vesselName": vesselName,
                "vesselId": self.g.get_vessel_Id(vesselName), "voyage": voyage, "portName": portName,
                "terminalName": terminalName, "customer": customer, "expectStartTime": str(nowTimeStamp) + a,
                "expectEndTime": str(timeStamp) + a, "expectBerthTime": str(nowTimeStamp) + a,
                "expectDepartureTime": str(timeStamp) + a, "description": description}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        # response
        self.outPut(url, data, r)
        msg = r.json()['msg']
        self.assertEqual(msg, '成功')
        # 将请求返回数据写入JSON文件
        self.s.write_sync('addTask', r.json()['data'])

    def test_04_start_task(self):
        """
        开始任务
        """
        global taskId
        taskInfo = self.s.read_loading('addTask')
        taskId = taskInfo['taskId']
        url = self.ip + '/task/index/startTask'
        headers = self.headers
        data = {
            'taskId': taskId,
            'taskType': self.taskType
        }
        r = requests.get(url, headers=headers, params=data)
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_05_sync(self):
        """
        同步外理数据
        """
        url = self.ip + '/task/lps/shwl/sync'
        headers = self.headers
        data = {
            "taskId": taskId
        }
        r = requests.get(url, headers=headers, params=data)
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')
