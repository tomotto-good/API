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

    def get_hatches(self, vesselId):
        """
        根据船舶ID获取舱口信息并写入JSON文件
        """
        url = self.ip + '/api/basic/getHatches'
        headers = self.headers
        data = {
            'vesselId': vesselId
        }
        r = requests.get(url, headers=headers, params=data)
        print("获取舱口信息请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        if r.json()['msg'] == '成功':
            self.s.write_loading('hatches', r.json()['data'])
            return self.s.read_loading('hatches')
        else:
            return False

    def get_spaces(self, vesselId):
        """
        根据船舶ID获取舱位信息并写入JSON文件
        """
        url = self.ip + '/api/basic/getSpaces'
        headers = self.headers
        data = {
            'vesselId': vesselId
        }
        r = requests.get(url, headers=headers, params=data)
        print("获取舱口信息请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        if r.json()['msg'] == '成功':
            self.s.write_loading('spaces', r.json()['data'])
            return self.s.read_loading('spaces')
        else:
            return False

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

    def get_oss_token(self):
        """
        获取ossToken并写入JSON文件
        """
        url = self.ip + '/api/file/getOSSToken'
        headers = self.headers
        r = requests.post(url, headers=headers)
        print("请求：{}\n返回：{} ".format(url, r.json()))
        # 将osstoken写入json中
        self.s.write_json('ossToken', r.json()['data'])

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
            if r.json()['msg'] == '成功':
                self.s.write_foot('detail', r.json()['data'])
                return self.s.read_foot('detail')
            else:
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                return False
        elif taskType == '2':
            # 获取监装PL信息
            plInfo = self.s.read_loading('pl')
            plId = plInfo[0]['plId']
            url = self.ip + '/task/lps/getPackListDetail'
            headers = self.headers
            data = {
                'taskId': taskId,
                'plId': plId,
            }
            r = requests.get(url, params=data, headers=headers)
            if r.json()['msg'] == '成功':
                self.s.write_loading('detail', r.json()['data'])
                # 返回监装明细信息
                return self.s.read_loading('detail')
            else:
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                return False

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
            if r.json()['msg'] == '成功':

                self.s.write_foot('pl', r.json()['data'])
                return self.s.read_foot('pl')
            else:
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                return False
        elif taskType == '5':
            url = self.ip + '/api/cgi/listPl'
            data = {
                'taskId': taskId
            }
            headers = self.headers
            r = requests.get(url, params=data, headers=headers)

            if r.json()['msg'] == '成功':
                self.s.write_collection('pl', r.json()['data'])
                return self.s.read_collection('pl')
            else:
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                return False
        elif taskType == '2':
            url = self.ip + '/task/lps/listPl'
            data = {
                'taskId': taskId
            }
            headers = self.headers
            r = requests.get(url, params=data, headers=headers)
            if r.json()['msg'] == '成功':
                self.s.write_loading('pl', r.json()['data'])
                return self.s.read_loading('pl')
            else:
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                return False
