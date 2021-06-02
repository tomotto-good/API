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
        # 获取data目录路径
        self.dataPath = os.path.join(self.APIPath, 'data')

    # 获取模板路径
    def get_pl_path(self, plName):
        return os.path.join(self.PlPath, plName + '.xlsx')

    # 获取配置文件路径
    def get_ini_path(self):
        return os.path.join(self.APIPath, 'config.ini')

    # 获取用户文件路径
    def get_json_path(self, fileName):
        return os.path.join(self.dataPath, fileName + '.json')

    # 获取打尺文件路径
    def get_foot_path(self, fileName):
        footPath = os.path.join(self.dataPath, 'foot')
        return os.path.join(footPath, fileName + '.json')

    # 获取集港文件路径
    def get_collection_path(self, fileName):
        collectionPath = os.path.join(self.dataPath, 'collection')
        return os.path.join(collectionPath, fileName + '.json')

    # 获取监装文件路径
    def get_loading_path(self, fileName):
        collectionPath = os.path.join(self.dataPath, 'loading')
        return os.path.join(collectionPath, fileName + '.json')

    # 获取监卸文件路径
    def get_unloading_path(self, fileName):
        collectionPath = os.path.join(self.dataPath, 'unloading')
        return os.path.join(collectionPath, fileName + '.json')
