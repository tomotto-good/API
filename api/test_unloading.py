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
            'Authorization': cls.token
        }

    @classmethod
    def tearDownClass(cls) -> None:
        """
        从数据库中删除任务
        """

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
        self.s.weite_unloading('addTask', r.json()['data'])

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
            msg = r.json()['msg']
            self.assertEqual(msg, '成功')

    @parameterized.expand(['15618994023', '17621209360'])
    @unittest.skip('跳过')
    def test_02_select_user(self, telephone):
        """
        根据手机号获取人员信息并添加执行人全部PL权限
        """
        url = self.ip + '/api/sysUserTask/getUserByPhoneAndCurrentUserAuthority'
        headers = {
            'os': self.os,
            'Authorization': self.token
        }
        data = {
            'taskId': taskId,
            'taskType': self.taskType,
            'phone': telephone,
            'areaCode': '86'
        }
        r = requests.get(url, headers=headers, params=data)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
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
        headers = {
            'os': self.os,
            'Authorization': self.token
        }
        data = {"areaCode": areaCode, "companyName": "", "delAuthority": 'null', "email": "",
                "headImg": headImg,
                "id": 'null', "jobName": "", "jobTitle": "", "name": name, "phone": phone, "plAuthority": plAuthority,
                "plAuthorityEdit": plAuthorityEdit, "plIds": plIds, "plScope": plScope, "plScopeEdit": plScopeEdit,
                "status": status,
                "taskAuthority": '3', "taskAuthorityEdit": 'true', "taskId": self.taskId,
                "taskType": self.taskType, "typeDesc": 'null',
                "updateAuthority": 'null', "userId": userId}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        self.assertEqual(r.json()['msg'], '成功')
        if telephone == '15618994023':
            print('添加兵哥成功')
        elif telephone == '17621209360':
            print('添加龙哥成功')

    @unittest.skip('跳过')
    def test_04_update_pl(self, fileName='数据存在符号'):
        """
        监卸任务-模板变更
        """
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        # 获取plId
        plId = self.g.get_plInfo(self.taskType, taskId)
        # 模板校验-获取pathKey
        pathKey = self.g.check_pl(taskId, self.taskType, fileName=fileName, plId=plId)
        if pathKey:
            url = self.ip + '/task/vds/updatePl'
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
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            self.assertEqual(r.json()['msg'], '成功')
