import json
from common.get_path import GetPath


class SaveJson:

    def write_json(self, fileName, data):
        jsonPath = GetPath().get_json_path(fileName=fileName)
        with open(jsonPath, 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False)
            print('写入成功:{}'.format(jsonPath))

    def read_json(self, fileName):
        jsonPath = GetPath().get_json_path(fileName=fileName)
        with open(jsonPath, 'r', encoding='utf-8')as f:
            return json.load(f)

    # 写入打尺任务文件
    def write_foot(self, fileName, data):
        footPath = GetPath().get_foot_path(fileName=fileName)
        with open(footPath, 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False)
            print('写入成功:{}'.format(footPath))

    # 读取打尺任务文件
    def read_foot(self, fileName):
        footPath = GetPath().get_foot_path(fileName=fileName)
        with open(footPath, 'r', encoding='utf-8')as f:
            return json.load(f)

    # 写入集港任务文件
    def write_collection(self, fileName, data):
        collectionPath = GetPath().get_collection_path(fileName=fileName)
        with open(collectionPath, 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False)
            print('写入成功:{}'.format(collectionPath))

    # 读取集港任务文件
    def read_collection(self, fileName):
        collectionPath = GetPath().get_collection_path(fileName=fileName)
        with open(collectionPath, 'r', encoding='utf-8')as f:
            return json.load(f)

    # 写入监装任务文件
    def write_loading(self, fileName, data):
        loadingPath = GetPath().get_loading_path(fileName=fileName)
        with open(loadingPath, 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False)
            print('写入成功:{}'.format(loadingPath))

    # 读取监装任务文件
    def read_loading(self, fileName):
        loadingPath = GetPath().get_loading_path(fileName=fileName)
        with open(loadingPath, 'r', encoding='utf-8')as f:
            return json.load(f)

    # 写入监卸任务文件
    def write_unloading(self, fileName, data):
        unloadingPath = GetPath().get_unloading_path(fileName=fileName)
        with open(unloadingPath, 'w', encoding='utf-8')as f:
            json.dump(data, f, ensure_ascii=False)
            print('写入成功:{}'.format(unloadingPath))

    # 读取监卸任务文件
    def read_unloading(self, fileName):
        unloadingPath = GetPath().get_unloading_path(fileName=fileName)
        with open(unloadingPath, 'r', encoding='utf-8')as f:
            return json.load(f)
