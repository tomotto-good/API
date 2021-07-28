import datetime
import json
import time
import unittest
import warnings
import requests
from common.getCommon import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestLoadingTime(unittest.TestCase):
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
    def tearDown(cls) -> None:
        pass

    @staticmethod
    def outPut(url, data, r):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    def test_01_get_time_log(self):
        """
        监装获取时间流
        """
        global taskId
        url = self.ip + '/task/lps/getTimeLog'
        headers = self.headers
        # 获取任务ID
        taskId = self.s.read_loading('addTask')['taskId']
        data = {
            'taskId': taskId
        }
        r = requests.get(url, headers=self.headers, params=data)
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')
        # 将时间流写入到json
        self.s.write_loading('timeLog', r.json()['data'])

    def test_02_update_time_log(self):
        """
        监装时间流修改
        """
        url = self.ip + '/task/lps/updateTimeLog'
        # 获取当前时间戳
        nowTime = datetime.datetime.now()
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        # 获取1天后的时间戳
        oneDayAgo = (datetime.datetime.now() + datetime.timedelta(days=1))
        oneTimeStamp = int(time.mktime(oneDayAgo.timetuple()))
        # 获取两天后时间戳
        twoDayAgo = (datetime.datetime.now() + datetime.timedelta(days=2))
        twoTimeStamp = int(time.mktime(twoDayAgo.timetuple()))
        # 获取三天后时间戳
        threeDayAgo = (datetime.datetime.now() + datetime.timedelta(days=3))
        threeTimeStamp = int(time.mktime(threeDayAgo.timetuple()))
        timeLog = self.s.read_loading('timeLog')
        for t in timeLog:
            # 预计靠泊时间
            if t['dataType'] == 1:
                dataId = t['dataId']
                data = [{"timeStamp": str(nowTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            # 实际靠泊时间
            elif t['dataType'] == 2:
                dataId = t['dataId']
                data = [{"timeStamp": str(oneTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            # 预计离港时间
            elif t['dataType'] == 7:
                dataId = t['dataId']
                data = [{"timeStamp": str(twoTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            # 实际离港时间
            elif t['dataType'] == 8:
                dataId = t['dataId']
                data = [{"timeStamp": str(threeTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            elif t['dataType'] == 3:
                dataId = t['dataId']
                data = [{"timeStamp": str(nowTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            # 实际靠泊时间
            elif t['dataType'] == 4:
                dataId = t['dataId']
                data = [{"timeStamp": str(oneTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            # 预计离港时间
            elif t['dataType'] == 5:
                dataId = t['dataId']
                data = [{"timeStamp": str(twoTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
            # 实际离港时间
            elif t['dataType'] == 6:
                dataId = t['dataId']
                data = [{"timeStamp": str(threeTimeStamp) + '000', "dataId": dataId}]
                r = requests.post(url, headers=self.headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                self.assertEqual(r.json()['msg'], '成功')
