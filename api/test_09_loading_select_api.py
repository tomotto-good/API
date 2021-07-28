import datetime
import time
import unittest
import warnings
import requests
import json

from parameterized import parameterized

from common.getCommon import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestLoadingSelectApi(unittest.TestCase):
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

    def test_01_select_before_loading(self):
        """
        （货物概况）查询
        """
        url = self.ip+'/task/lps/getBeforeLoading'
        headers = self.headers

