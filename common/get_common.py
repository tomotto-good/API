import json
import time
import datetime
import warnings
import requests
from common.read_ini import ReadIni
from common.get_path import GetPath
from common.save_json import SaveJson


class GetCommon:
    def __init__(self):
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        self.s = SaveJson()
        self.g = GetPath()
        self.ip = r.get_ip()

        # 获取登录的类型
        self.os = r.get_os()
        # 获取token
        self.token = r.get_token()
        # 设置请求体
        self.headers = {
            'os': self.os,
            'Authorization': self.token
        }

    def get_vessel_Id(self, vesselName):
        """
        获取系统内船信息并写入JSON文件
        -通过vesselName获取vesselId
        """
        url = self.ip + '/api/basic/getVesselList'
        headers = self.headers
        r = requests.post(url, headers=headers)
        print("请求：{}\n返回：{} ".format(url, r.json()))
        self.s.write_json('vessel', r.json()['data'])
        vessel = self.s.read_json('vessel')
        for i in vessel:
            if i['vesselName'] == vesselName:
                return i['vesselId']

    def get_areaList(self):
        """
        获取系统内场地Id/名称，返回列表
        """

        url = self.ip + '/api/basic/getAreaList'
        headers = self.headers
        data = {
            'terminalId': '1'
        }
        r = requests.get(url, headers=headers, params=data)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        areaList = r.json()['data']
        b = []
        for i in areaList:
            a = {}
            a['areaId'] = i['areaId']
            a['areaName'] = i['region'] + i['number']
            b.append(a)
        self.s.write_json('areaList', b)
        data = self.s.read_json('areaList')
        return data

    def check_pl(self, taskId, taskType, fileName, plId=None):
        """
        模板校验接口：/task/system/check
        """
        url = self.ip + '/task/system/check'
        filePath = self.g.get_pl_path(fileName)
        files = {
            'file': open(filePath, 'rb'),
        }
        headers = self.headers
        data = {
            'taskId': taskId,
            'taskType': taskType,
            'plId': plId
        }
        r = requests.post(url, headers=headers, files=files, data=data)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        msg = r.json()['data']['desc']
        if msg == '文件上传成功':
            pathKey = r.json()['data']['path']
            return pathKey
        else:
            print("文件校验失败：{}".format(r.json()))

    def get_detailInfo(self, taskId, taskType):
        """
        根据任务类型获取明细信息并写如入JSON
        """
        if taskType == '1':
            plInfo = self.s.read_foot('pl')
            plId = plInfo[0]['plId']
            url = self.ip + '/api/mms/getPackListDetail'
            headers = self.headers
            data = {
                'taskId': taskId,
                'plId': plId,
            }
            r = requests.get(url, params=data, headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            self.s.write_foot('detail', r.json()['data'])
            print('写入成功:{}'.format(self.g.get_foot_path('detail')))
            return self.s.read_foot('detail')

    def get_plInfo(self, taskId, taskType):
        """
        根据任务类型获取PL信息写入JSON并返回出来
        """
        if taskType == '1':
            url = self.ip + '/api/mms/listPl'
            data = {
                'taskId': taskId
            }
            headers = self.headers
            r = requests.get(url, params=data, headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            self.s.write_foot('pl', r.json()['data'])
            return self.s.read_foot('pl')
        elif taskType == '5':
            url = self.ip + '/api/cgi/listPl'
            data = {
                'taskId': taskId
            }
            headers = self.headers
            r = requests.get(url, params=data, headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            self.s.write_foot('pl', r.json()['data'])
            return self.s.read_foot('pl')
