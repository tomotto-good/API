#!/usr/bin/python
# -*- coding:utf-8 -*-
import unittest
import warnings
import requests
import json
from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson
from parameterized import parameterized


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
            'Authorization': cls.token,
            'versionName': '1.6.11'
        }
        # 获取ossPath
        cls.ossPath = r.get_oss_path()
        # 获取打尺图片path
        cls.detailPicturePath = r.get_foot_picture_path('detail')
        cls.overAllPath = r.get_foot_picture_path('overall')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        从数据库中删除任务
        """
        pass

    @staticmethod
    def outPut(url, data, r):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    @parameterized.expand(['1', '2'])
    def test_01_foot_picture(self, photoType):
        """
        上传清单内前5条明细照片
        """
        global taskId
        taskInfo = self.c.read_foot('addTask')
        taskId = taskInfo['taskId']
        url = self.ip + '/api/mms/uploadPlImages'
        headers = self.headers
        # 获取明细信息
        detailInfo = self.g.get_detailInfo(taskId, self.taskType)

        for i in detailInfo[0:5]:
            if photoType == '2':
                plId = i['plId']
                plDetailId = i['plDetailId']
                path = self.detailPicturePath
                ossUrl = self.ossPath + self.detailPicturePath
                data = [{
                    "address": "numberDetail",
                    "path": path,
                    "photoRemark": "明细照片备注",
                    "photoType": photoType,
                    "plDetailId": plDetailId,
                    "plId": plId,
                    "taskId": taskId,
                    "url": ossUrl
                }]
                r = requests.post(url, headers=headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                # 断言
                self.assertEqual(r.json()['msg'], '成功')
            elif photoType == '1':
                plId = i['plId']
                path = self.overAllPath
                ossUrl = self.ossPath + self.overAllPath
                data = [{
                    "path": path,
                    "photoRemark": "整体照片备注",
                    "photoType": photoType,
                    "taskId": taskId,
                    "plId": plId,
                    "url": ossUrl
                }]
                r = requests.post(url, headers=headers, data=json.dumps(data))
                print(self.outPut(url, data, r))
                # 断言
                self.assertEqual(r.json()['msg'], '成功')
