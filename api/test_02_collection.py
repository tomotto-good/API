import datetime
import time
import unittest
import warnings
import requests
import json
from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson
from tools.MyEncoder import MyEncoder

from parameterized import parameterized


class TestCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.m = MyEncoder()
        cls.s = SaveJson()
        # 获取环境
        cls.ip = r.get_ip()
        # 设置任务类型
        cls.taskType = '5'
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
            taskName = '安卓/集港'
        elif self.os == '2':
            taskName = 'IOS/集港'
        data = {"taskName": taskName, "taskType": self.taskType, "vesselName": vesselName,
                "vesselId": self.g.get_vessel_Id(vesselName), "voyage": voyage, "portName": portName,
                "terminalName": terminalName, "customer": customer, "expectStartTime": str(nowTimeStamp) + a,
                "expectEndTime": str(timeStamp) + a, "expectBerthTime": str(nowTimeStamp) + a,
                "expectDepartureTime": str(timeStamp) + a, "description": description}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        # 将请求数据
        print(self.outPut(url, data, r))
        msg = r.json()['msg']
        self.assertEqual(msg, '成功')
        # 将请求返回数据写入JSON文件
        self.s.write_collection('addTask', r.json()['data'])

    @parameterized.expand([('清单1', '标准模板'), ('清单2', '数据存在符号')])
    def test_02_import_pl(self, shippingOrder, fileName):
        """
        验证集港任务--模板导入
        """
        global taskId
        taskInfo = self.s.read_collection('addTask')
        taskId = taskInfo['taskId']
        pathKey = self.g.check_pl(taskId, self.taskType, fileName=fileName)
        if pathKey:
            url = self.ip + '/task/cgi/createPl'
            data = {"taskId": taskId, "shippingOrder": shippingOrder, "lengthUnit": 2, "weightUnit": 1,
                    "pathKey": pathKey}
            headers = self.headers
            r = requests.post(url, data=json.dumps(data), headers=headers)
            # response
            self.outPut(url, data, r)
            msg = r.json()['msg']
            self.assertEqual(msg, '成功')
            # 将PL信息写入JSON
            self.g.get_plInfo(taskId, self.taskType)
            return taskId
        else:
            print("清单校验失败")

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

    def test_05_collection(self):
        """
        对前5条明细进行集港操作
        """
        # 获取系统内场地信息
        areaInfo = self.g.get_areaList()[6]
        areaId = areaInfo['areaId']
        areaName = areaInfo['areaName']
        url = self.ip + '/api/cgi/finishDetails'
        headers = self.headers
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        detailInfo = self.g.get_detailInfo(taskId, self.taskType)
        for i in detailInfo[0:5]:
            plId = i['plId']
            plDetailId = i['plDetailId']
            data = [{"taskId": taskId, "areaId": areaId, "realCgiFinishTime": str(nowTime), "remark": "明细备注",
                     "plId": plId, "licensePlateNumber": "鲁D3638U", "plDetailId": plDetailId, "areaName": areaName,
                     "abnormal": "17"},
                   ]
            data = json.dumps(data, ensure_ascii=False)
            r = requests.post(url, headers=headers, data=data.encode('utf-8'))
            print(self.outPut(url, data, r))
            self.assertEqual(r.json()['msg'], '成功')
