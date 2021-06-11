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


class TestUnloading(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.s = SaveJson()
        # 设置环境
        cls.ip = r.get_ip()
        # 设置任务类型
        cls.taskType = '3'
        # 设置登录的类型
        cls.os = r.get_os()
        # 从配置文件中获取token
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
        pass

    @staticmethod
    def outPut(url, data, r):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    @parameterized.expand([('杨敏馨测试1', 'Sos', 'Shanghai Port', '军工路码头', '任务描述', '顾鹏')])
    def test_01_add_task(self, vesselName, voyage, portName, terminalName, description, customer):
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
            taskName = '安卓/监卸'
        elif self.os == '2':
            taskName = 'IOS/监卸'
        data = {"taskName": taskName, "taskType": self.taskType, "vesselName": vesselName,
                "vesselId": self.g.get_vessel_Id(vesselName), "voyage": voyage, "portName": portName,
                "terminalName": terminalName, "customer": customer, "expectStartTime": str(nowTimeStamp) + a,
                "expectEndTime": str(timeStamp) + a, "expectBerthTime": str(nowTimeStamp) + a,
                "expectDepartureTime": str(timeStamp) + a, "description": description}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        # response
        print(self.outPut(url, data, r))
        msg = r.json()['msg']
        self.assertEqual(msg, '成功')
        # 将请求返回数据写入JSON文件
        self.s.write_unloading('addTask', r.json()['data'])

    @parameterized.expand([('清单1', '标准模板'), ('清单2', '数据存在符号')])
    def test_02_import_pl(self, shippingOrder, fileName):
        """
        验证监卸任务--模板导入
        """
        global taskId
        # 获取任务ID
        taskInfo = self.s.read_unloading('addTask')
        taskId = taskInfo['taskId']
        # 获取港口/码头
        portName = taskInfo['portName']
        terminalName = taskInfo['terminalName']
        pathKey = self.g.check_pl(taskId, self.taskType, fileName=fileName)
        if pathKey:
            url = self.ip + '/task/vds/createPl'
            data = {"taskId": taskId, "shippingOrder": shippingOrder, "lengthUnit": 0, "weightUnit": 0,
                    "pathKey": pathKey, 'taskType': self.taskType, 'portName': portName, 'terminalName': terminalName}
            headers = {
                'os': self.os,
                'Authorization': self.token,
                'versionCode': '372',
                'versionName': '1.7.4.3'
            }
            r = requests.post(url, json=data, headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            self.assertEqual(r.json()['msg'], '成功')

    def test_04_collection(self):
        """
        开始任务
        """
        url = self.ip + '/task/index/startTask'
        headers = self.headers
        data = {
            'taskId': taskId,
            'taskType': self.taskType
        }
        r = requests.get(url, headers=headers, params=data)
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')
