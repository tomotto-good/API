import configparser
from common.get_path import GetPath


class ReadIni:
    def __init__(self):
        self.c = GetPath().get_ini_path()
        self.config = configparser.ConfigParser()
        self.config.read(self.c, encoding="utf-8")

    def write_ini(self, token):
        if 'token' in self.config.sections():
            # 添加键名/值
            self.config.set('token', 'token', token)
            self.config.write(open(self.c, 'r+'))
        else:
            # 添加文件节点
            self.config.add_section('token')
            # 添加键名/值
            self.config.set('token', 'token', token)
            self.config.write(open(self.c, 'r+'))

    def get_os(self):
        os = self.config.get("os", "os")
        return os

    def get_token(self):
        token = self.config.get('token', 'token')
        return token

    def get_ip(self):
        ip = self.config.get('ip', 'ip')
        return ip

    def get_user(self):
        user = self.config.get('user', 'phone')
        return user
