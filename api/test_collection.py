import datetime
import time
import unittest
import warnings
import requests
import json
from common.get_common import GetCommon
from common.read_ini import ReadIni
from tools.MyEncoder import MyEncoder

from parameterized import parameterized


class TestCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.m = MyEncoder()
        # 获取环境
        cls.ip = r.get_ip()
        # 设置任务类型
        cls.taskType = '5'
        # 设置登录的类型
        cls.os = r.get_os()
        # 获取token
        cls.token = r.get_token()
        # 获取添加的任务ID
        cls.taskId = cls.g.get_taskId(cls.taskType)
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

    def test_01_import_pl(self, fileName='标准模板'):
        """
        验证集港任务--模板导入
        """

        pathKey = self.g.check_pl(self.taskId, self.taskType, fileName=fileName)
        if pathKey:
            url = self.ip + '/task/cgi/createPl'
            data = {"taskId": self.taskId, "shippingOrder": "清单1", "lengthUnit": 2, "weightUnit": 1,
                    "pathKey": pathKey}
            headers = self.headers
            r = requests.post(url, data=json.dumps(data), headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            msg = r.json()['msg']
            self.assertEqual(msg, '成功')
        else:
            print('模板校验失败')

    # @unittest.skip('跳过')
    # def test_02_get_pl_info(self):
    #     """
    #     根据任务ID获取PL信息
    #     """
    #     url = self.ip + '/api/cgi/listPl'
    #     headers = self.headers
    #     data = {
    #         'taskId': self.taskId
    #     }
    #     r = requests.get(url, headers=headers, params=data)
    #     if r.json()['msg'] == '成功':
    #         print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
    #         response = r.json()['data'][0]
    #         plId = response['plId']
    #     else:
    #         print('获取plId失败：{}'.format(r.json()))

    @parameterized.expand(['15618994023', '17621209360'])
    def test_02_select_user(self, telephone):
        """
        根据手机号获取人员信息并添加执行人全部PL权限
        """
        url = self.ip + '/api/sysUserTask/getUserByPhoneAndCurrentUserAuthority'
        headers = self.headers
        data = {
            'taskId': self.taskId,
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
        headers = self.headers
        data = {"areaCode": areaCode, "companyName": "", "delAuthority": 'null', "email": "",
                "headImg": headImg,
                "id": 'null', "jobName": "", "jobTitle": "", "name": name, "phone": phone, "plAuthority": plAuthority,
                "plAuthorityEdit": plAuthorityEdit, "plIds": plIds, "plScope": plScope, "plScopeEdit": plScopeEdit,
                "status": status,
                "taskAuthority": '3', "taskAuthorityEdit": 'true', "taskId": self.taskId,
                "taskType": self.taskType, "typeDesc": 'null',
                "updateAuthority": 'null', "userId": userId}
        r = requests.post(url, data=json.dumps(data, cls=MyEncoder, indent=4), headers=headers)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        self.assertEqual(r.json()['msg'], '成功')
        if telephone == '15618994023':
            print('添加兵哥成功')
        elif telephone == '17621209360':
            print('添加龙哥成功')

    def test_03_update_pl(self, fileName='数据存在符号'):
        """
        集港任务-模板变更
        """
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        # 获取plId
        plId = self.g.get_plId(self.taskType, self.taskId)
        # 模板校验-获取pathKey
        pathKey = self.g.check_pl(self.taskId, self.taskType, fileName=fileName, plId=plId)
        if pathKey:
            url = self.ip + '/task/cgi/updatePl'
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
                    "shippingOrder": "清单1", "status": '0', "taskId": self.taskId, "taskType": self.taskType,
                    "terminalId": 'null',
                    "terminalName": "军工路码头", "unread": '0', "updateTimeStamp": str(nowTimeStamp) + '0',
                    "updaterName": "顾鹏",
                    "vesselId": '63', "vesselName": "杨敏馨测试1", "voyage": "SOS", "lengthUnit": '2', "weightUnit": '1',
                    "pathKey": pathKey}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            self.assertEqual(r.json()['msg'], '成功')
