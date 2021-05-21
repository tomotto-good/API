import unittest
import time
from BeautifulReport import BeautifulReport as bf

# 组装测试套件
suite = unittest.defaultTestLoader.discover("./api", pattern="test*.py")
# 制定测试报告存放路径及名称
file_path = "./report/莫斯接口测试报告{}.html".format(time.strftime("%Y_%m_%d"))
# 运行测试套件并生成测试报告
with open(file_path, "wb") as f:
    runner = bf(suite)
    runner.report(filename=file_path, description='莫斯接口测试')
    f.close()
