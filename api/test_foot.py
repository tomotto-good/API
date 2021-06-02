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
        cls.ip = r.get_ip()
        cls.c = SaveJson()
        cls.taskType = '1'
        # 设置登录的类型
        cls.os = r.get_os()
        cls.token = r.get_token()
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
        return "'\033[1;31;40m请求\033[0m'：{} \n'\033[1;31;40m数据\033[0m':{} \n'\033[1;31;40m返回\033[0m'：{} ".format(url,
                                                                                                                 data,
                                                                                                                 r.json())

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

    @parameterized.expand(['15618994023', '17621209360'])
    @unittest.skip('跳过')
    def test_03_add_user(self, telephone):
        """
        根据手机号获取人员信息并添加执行人全部PL权限
        """
        url = self.ip + '/api/sysUserTask/getUserByPhoneAndCurrentUserAuthority'
        headers = self.headers
        data = {
            'taskId': taskId,
            'taskType': self.taskType,
            'phone': telephone,
            'areaCode': '86'
        }
        r = requests.get(url, headers=headers, params=data)
        # response
        self.outPut(url, data, r)
        results = r.json()['data']
        self.assertEqual(r.json()['msg'], '成功')
        areaCode = results['areaCode']
        headImg = results['headImg']
        name = results['name']
        phone = results['mobile']
        plAuthority = results['plAuthority']
        plAuthorityEdit = results['plAuthorityEdit']
        plScope = results['plScope']
        plScopeEdit = results['plScopeEdit']
        status = results['status']
        plIds = results['plIds']
        userId = results['userId']
        url = self.ip + '/api/sysUserTask/addUserTaskRel'
        headers = self.headers
        data = {"areaCode": areaCode, "companyName": "", "delAuthority": 'null', "email": "",
                "headImg": headImg,
                "id": 'null', "jobName": "", "jobTitle": "", "name": name, "phone": phone, "plAuthority": plAuthority,
                "plAuthorityEdit": plAuthorityEdit, "plIds": plIds, "plScope": plScope, "plScopeEdit": plScopeEdit,
                "status": status,
                "taskAuthority": '3', "taskAuthorityEdit": 'true', "taskId": taskId,
                "taskType": self.taskType, "typeDesc": 'null',
                "updateAuthority": 'null', "userId": userId}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.outPut(url, data, r)
        self.assertEqual(r.json()['msg'], '成功')
        if telephone == '15618994023':
            print('添加兵哥成功')
        elif telephone == '17621209360':
            print('添加龙哥成功')

    @unittest.skip('跳过')
    def test_04_update_pl(self, fileName='数据存在符号'):
        """
        打尺任务-模板变更
        """
        global plId
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        # 获取plId
        plInfo = self.g.get_plInfo(taskId, self.taskType)
        plId = plInfo[0]['plId']
        # 模板校验-获取pathKey
        pathKey = self.g.check_pl(taskId, self.taskType, fileName=fileName, plId=plId)
        if pathKey:
            url = self.ip + '/task/mms/updatePl'
            headers = self.headers
            data = {"acceptanceNumber": "", "bargePositionNo": 'null', "consignee": "", "contractNumber": "",
                    "createTimeStamp": str(nowTimeStamp) + '000', "creatorName": "顾鹏", "deliveryAddress": "",
                    "description": "",
                    "dischargingPort": "", "expectArriveTime": 'null', "expectArriveTimeStamp": 'null',
                    "finishTotalQty": '0',
                    "finishTotalVolume": '0', "finishTotalWeight": '0', "groupId": "", "importTotalQty": '9',
                    "importTotalVolume": '517.42', "importTotalWeight": '6.97', "increase": '-88',
                    "increment": '-458.4',
                    "loadingPort": "", "owner": "", "phone": "", "picGroupId": 'null', "plAuthority": '1', "plId": plId,
                    "plNumber": "PL8000000639269885", "portId": 'null', "portName": "Shanghai Port",
                    "realCgiEndTime": 'null',
                    "realCgiEndTimeStamp": 'null', "realCgiStartTime": 'null', "realCgiStartTimeStamp": 'null',
                    "shipper": "",
                    "shippingOrder": "清单1", "status": '0', "taskId": taskId, "taskType": self.taskType,
                    "terminalId": 'null',
                    "terminalName": "军工路码头", "unread": '0', "updateTimeStamp": str(nowTimeStamp) + '0',
                    "updaterName": "顾鹏",
                    "vesselId": '63', "vesselName": "杨敏馨测试1", "voyage": "SOS", "lengthUnit": '2', "weightUnit": '1',
                    "pathKey": pathKey}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            # response
            self.outPut(url, data, r)
            self.assertEqual(r.json()['msg'], '成功')

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
        areaInfo = self.g.get_areaList()[0]
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
                     "realWidth": realWidth, "abnormal": abnormal}]
            data = json.dumps(data, ensure_ascii=False)
            r = requests.post(url, headers=headers, data=data.encode('utf-8'))
            print(self.outPut(url, data, r))
            self.assertEqual(r.json()['msg'], '成功')

    @parameterized.expand([('0', '2060', '1060', '明细备注', '860')])
    def test_09_foot(self, abnormal, realLength, realHeight, remark, realWidth):
        """
        批量调整尺寸
        """
        # 获取系统内场地信息
        areaInfo = self.g.get_areaList()[1]
        areaId = areaInfo['areaId']
        areaName = areaInfo['areaName']
        url = self.ip + '/api/mms/measured'
        headers = self.headers
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        detailInfo = self.c.read_foot('detail')
        for i in detailInfo[5:10]:
            plId = i['plId']
            plDetailId = i['plDetailId']
            data = [{"taskId": taskId, "realLength": realLength, "areaId": areaId, "realHeight": realHeight,
                     "areaName": areaName,
                     "measureTime": nowTime, "remark": remark, "plId": plId, "plDetailId": plDetailId,
                     "realWidth": realWidth, "abnormal": abnormal}]
            data = json.dumps(data, ensure_ascii=False)
            r = requests.post(url, headers=headers, data=data.encode('utf-8'))
            print(self.outPut(url, data, r))
            self.assertEqual(r.json()['msg'], '成功')
            print("{} 打尺成功".format(i['shippingMark']))
