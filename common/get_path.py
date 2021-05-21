import os


class GetPath:
    def __init__(self):
        # 当前文件绝对路径
        curPath = os.path.realpath(__file__)
        # 当前文件夹绝对路径
        self.dirPath = os.path.dirname(curPath)
        # 获取PL目录路径
        self.APIPath = os.path.dirname(self.dirPath)
        self.PlPath = os.path.join(self.APIPath, 'pl')
        # 获取common目录路径
        self.CommonPath = os.path.join(self.APIPath, 'common')

    # 获取模板路径
    def get_pl_path(self, plName):
        return os.path.join(self.PlPath, plName + '.xlsx')

    # 获取配置文件路径
    def get_ini_path(self):
        return os.path.join(self.CommonPath, 'common.ini')
