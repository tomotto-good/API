import datetime
import json
import time
import unittest
import warnings

import requests

from common.getCommon import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestCollectionPicture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.c = SaveJson()
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
        # 获取集港图片path
        cls.detailPath = r.get_collection_picture_path('detail')
        cls.overAllPath = r.get_collection_picture_path('overall')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @staticmethod
    def outPut(url, data, r):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    def test_001_collection_picture(self):
        """
        上传集港前五条明细照片
        """
        global taskId
        # 获取任务ID
        taskInfo = self.c.read_collection('addTask')
        taskId = taskInfo['taskId']
        url = self.ip + '/api/cgi/uploadDetailPicture'
        headers = self.headers
        # 获取明细信息
        detailInfo = self.g.get_detailInfo(taskId, self.taskType)
        for i in detailInfo[0:5]:
            plId = i['plId']
            plDetailId = i['plDetailId']
            data = [
                {
                    "fileType": 2,
                    'name': '白骨精.jpg',
                    "plDetailId": plDetailId,
                    "plId": plId,
                    "remark": "明细照片备注",
                    "takePhotoDate": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    "url": self.detailPath
                }
            ]
            r = requests.post(url, headers=headers, data=json.dumps(data))
            print(self.outPut(url, data, r))

    def test_002_collection_picture(self):
        """
        上传集港整体照片
        """
        # 读取PL信息
        plInfo = self.c.read_collection('pl')
        url = self.ip + '/api/cgi/uploadPlPicture'
        headers = self.headers
        plId = plInfo[0]['plId']
        data = [
            {
                "fileType": 2,
                'name': '猪八戒.jpg',
                "plDetailId": '',
                "plId": plId,
                "remark": "整体照片备注",
                "takePhotoDate": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                "url": self.overAllPath
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
