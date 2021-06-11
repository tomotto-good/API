import unittest
import time
from BeautifulReport import BeautifulReport as bf
from common.get_path import GetPath


class runAll:
    def __init__(self):
        self.path = GetPath()
        # 测试报告存放路径
        self.reportPath = self.path.get_report_path()
        # 测试用例存放路径
        self.apiPath = self.path.apiPath

    def run_all(self):
        # 组装测试套件
        suite = unittest.defaultTestLoader.discover(self.apiPath, pattern="test*")
        file_path = self.reportPath
        # 运行测试套件并生成测试报告
        with open(file_path, "wb") as f:
            runner = bf(suite)
            runner.report(filename='./report/莫斯API测试报告{}.html'.format(time.strftime("%Y_%m_%d")), description='莫斯接口测试')
            f.close()


if __name__ == '__main__':
    runAll().run_all()
