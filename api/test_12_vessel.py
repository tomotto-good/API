import requests
import unittest
from common.read_ini import ReadIni


class Test_vessel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        r = ReadIni()
        cls.ip = r.get_ip()
        cls.os = r.get_os()
        cls.token = r.get_token()
        cls.headers = {
            'os': cls.os,
            'Authorization': cls.token,
            'versionName': '1.6.11'
        }

    def test_01_vessel(self, vesselId='63'):
        """
        查看船舶结构
        """
        url = self.ip + '/api/basic/getVesselStructure'
        data = {
            'vesselId': vesselId
        }
        headers = self.headers
        r = requests.get(url, headers=headers, params=data)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        self.assertEqual(r.json()['msg'], '成功')
