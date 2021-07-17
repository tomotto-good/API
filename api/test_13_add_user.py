#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import unittest
import warnings
import requests
from parameterized import parameterized
from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestAddUser(unittest.TestCase):
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
            'Authorization': cls.token,
            'versionName': '1.7.0'
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

    def test_01_select_user_authority(self, phone='15618994023'):
        """
        新增人员-根据手机号查询用户&查询当前登录人新增或编辑人员时的权限（自己的权限）
        """
        global footTaskId, footTaskType
        footTaskInfo = self.c.read_foot('addTask')
        footTaskId = footTaskInfo['taskId']
        footTaskType = footTaskInfo['taskType']
        url = self.ip + '/api/sysUserTask/getUserByPhoneAndCurrentUserAuthority'
        headers = self.headers
        data = {
            'phone': phone,
            'taskId': footTaskId,
            'taskType': footTaskType
        }
        r = requests.get(url, headers=headers, params=data)
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    @parameterized.expand([('15618994023', '1', '1', '2'), ('17621209360', '1', '1', '3')])
    def test_02_add_user(self, phone, plScope, taskAuthority, plAuthority):
        """
        新增人员
        """
        url = self.ip + '/task/sysUserTask/addUserTaskRel'
        headers = self.headers
        data = {
            "areaCode": "+86",
            "companyId": 0,
            "phone": phone,  # 「新增使用-必填」用户手机号
            "phoneList": [],  # 「（多选）拉企业用户进入任务」用户手机号数组
            "plAuthority": plAuthority,  # pl权限:2执行,3查看
            "plIds": [],  # 如果pl范围为部分，则需要传入选中的pl
            "plScope": plScope,  # pl范围:1所有,2部分
            "taskAuthority": taskAuthority,  # 任务权限:3执行,1查看
            "taskId": footTaskId,  # 任务id
            "taskType": footTaskType,  # 任务类型
            "userId": 0  # 「更新使用-必填」要更新的用户id
        }
        r = requests.post(
            url, headers=headers, data=json.dumps(data)
        )
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')
