#!/usr/bin/python
# -*- coding:utf-8 -*-

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


class TestFoot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.c = SaveJson()
        # 获取环境
        cls.ip = r.get_ip()
        # 设置任务类型
        cls.taskType = '1'
        # 设置登录的类型
        cls.os = r.get_os()
        # 获取token
        cls.token = r.get_token()
        # 设置请求头
        cls.headers = {
            'os': cls.os,
            'Authorization': cls.token
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
            taskName = '安卓/打尺'
        elif self.os == '2':
            taskName = 'IOS/打尺'
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
        self.c.write_foot('addTask', r.json()['data'])

    @parameterized.expand([('清单1', '标准模板')])
    def test_02_import_pl(self, shippingOrder, fileName):
        """
        验证打尺任务--模板导入
        """
        global taskId
        taskInfo = self.c.read_foot('addTask')
        taskId = taskInfo['taskId']
        pathKey = self.g.check_pl(taskId, self.taskType, fileName=fileName)
        if pathKey:
            url = self.ip + '/task/mms/createPl'
            data = {"taskId": taskId, "shippingOrder": shippingOrder, "lengthUnit": 2, "weightUnit": 1,
                    "pathKey": pathKey}
            headers = self.headers
            r = requests.post(url, data=json.dumps(data), headers=headers)
            # response
            self.outPut(url, data, r)
            msg = r.json()['msg']
            self.assertEqual(msg, '成功')
            self.g.get_plInfo(taskId, self.taskType)
            return taskId
        else:
            print("清单校验失败")

    def test_07_foot(self):
        """
        开始任务
        """
        url = self.ip + '/task/index/startTask'
        data = {
            'taskId': taskId,
            'taskType': self.taskType
        }
        headers = self.headers
        r = requests.get(url, headers=headers, params=data)
        self.outPut(url, data, r)
        self.assertEqual(r.json()['msg'], '成功')

    @parameterized.expand([('17', '2060', '1060', '明细备注', '860')])
    def test_08_foot(self, abnormal, realLength, realHeight, remark, realWidth):
        """
        对清单内前5条明细进行异常打尺
        """
        # 获取系统内场地信息
        areaInfo = self.g.get_areaList()[6]
        areaId = areaInfo['areaId']
        areaName = areaInfo['areaName']
        url = self.ip + '/api/mms/measured'
        headers = self.headers
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        detailInfo = self.g.get_detailInfo(taskId, self.taskType)
        for i in detailInfo[0:5]:
            plId = i['plId']
            plDetailId = i['plDetailId']
            data = [{"taskId": taskId, "realLength": realLength, "areaId": areaId, "realHeight": realHeight,
                     "areaName": areaName,
                     "measureTime": nowTime, "remark": remark, "plId": plId, "plDetailId": plDetailId,
                     "realWidth": realWidth, 'abnormal': abnormal}]
            data = json.dumps(data, ensure_ascii=False)
            r = requests.post(url, headers=headers, data=data.encode('utf-8'))
            print(self.outPut(url, data, r))
            self.assertEqual(r.json()['msg'], '成功')

    def test_09_foot(self):
        """
        上传照片-清单内前5张照片
        """
        url = self.ip + '/api/mms/uploadPlImages'
        headers = self.headers
        # 获取明细信息
        detailInfo = self.g.get_detailInfo(taskId, self.taskType)
        for i in detailInfo[0:5]:
            plId = i['plId']
            plDetailId = i['plDetailId']
            data = [{
                "address": "场地号number",
                "path": "13/task/mms/92/186/16254/4293e7d8-84e4-4df1-ba1a-cd747a5099f0.jpg",
                "photoRemark": "照片备注",
                "photoType": 2,
                "plDetailId": plDetailId,
                "plId": plId,
                "taskId": taskId,
                "url": "http://oss.mars-tech.com.cn/13/task/mms/92/186/16254/4293e7d8-84e4-4df1-ba1a-cd747a5099f0.jpg"
            }]
            r = requests.post(url, headers=headers, data=json.dumps(data))
            print(self.outPut(url, data, r))
            # 断言
            self.assertEqual(r.json()['msg'], '成功')
