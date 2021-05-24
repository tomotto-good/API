import json

from common.get_path import GetPath
import pickle


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
