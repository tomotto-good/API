import unittest
import warnings
import requests
import json
from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestLoadingPlStowageData(unittest.TestCase):
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
    def outPut(url, data, r):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    def test_loading_pl_stowage(self):
        """
        分票录入积载数据
        """
        url = self.ip + '/task/lps/entryPlStowageData'
        headers = self.headers
        # 获取plId
        plInfo = self.s.read_loading('pl')
        plId = plInfo[0]['plId']
        # 获取TaskId
        taskInfo = self.s.read_loading('addTask')
        taskId = taskInfo['taskId']
        # 获取工班ID
        groupInfo = self.s.read_loading('group')
        groupId = groupInfo['groupId']
        # 获取spaces信息
        spacesInfo = self.s.read_loading('spaces')
        #  获取hatch信息
        hatchInfo = self.s.read_loading('hatches')
        for i in spacesInfo:
            for hatch in hatchInfo:
                if i['hatchId'] == hatch['hatchId']:
                    hatchName = hatch['hatchName']
                    spaceName = i['spaceName']
                    data = [
                        {
                            "dataType": '3',  # 数据类型 1：预配载数据3：实时积载数据
                            "groupId": groupId,  # 工班ID
                            "hatchId": i['hatchId'],
                            "hatchName": hatchName,
                            "plId": plId,
                            "quantity": '8',  # 舱口货物数量
                            "spaceId": i['spaceId'],
                            "spaceName": spaceName,
                            "taskId": taskId,
                            "volume": '9',
                            "weight": '10'
                        }
                    ]
                    r = requests.post(url, headers=headers, data=json.dumps(data))
                    print(self.outPut(url, data, r))
                    self.assertEqual(r.json()['msg'], '成功')
