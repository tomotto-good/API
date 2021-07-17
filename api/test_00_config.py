import unittest
import warnings
from common.read_ini import ReadIni


class TestCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        # 获取登录ip
        cls.ip = r.get_ip()
        # 设置登录的类型
        cls.os = r.get_os()
        # 获取手机号
        cls.user = r.get_user()

    def test_config(self):
        """
        初始化配置
        """
        if self.ip == 'http://192.168.1.13:3080':
            print("环境：测试")
        elif self.ip == 'http://api.pre.mars-tech.com.cn':
            print("环境：预发布")
        elif self.ip == 'https://api.mars-tech.com.cn':
            print("环境：正式")
        if self.os == '1':
            print("客户端: 安卓")
        elif self.os == '2':
            print("客户端: IOS")
        print('当前登录用户为:{}'.format(self.user))
