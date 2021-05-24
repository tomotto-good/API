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
        self.s.write_json('vessel', r.json()['data'])
        vessel = self.s.read_json('vessel')
        for i in vessel:
            if i['vesselName'] == vesselName:
                return i['vesselId']

    def get_taskId(self, taskType):
        """
        验证Ios添加任务
        """
        global taskName
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        threeDayAgo = (datetime.datetime.now() + datetime.timedelta(days=7))
        # 获取7天后的时间戳
        timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        a = '000'
        url = self.ip + '/task/index/addTask.json'
        headers = self.headers
        if self.os == '1':
            if taskType == '1':
                taskName = '安卓/打尺'
            elif taskType == '2':
                taskName = '安卓/监装'
            elif taskType == '3':
                taskName = '安卓/监卸'
            elif taskType == '5':
                taskName = '安卓/集港'
        elif self.os == '2':
            if taskType == '1':
                taskName = 'IOS/打尺'
            elif taskType == '2':
                taskName = 'IOS/监装'
            elif taskType == '3':
                taskName = 'IOS/监卸'
            elif taskType == '5':
                taskName = 'IOS/集港'

        data = {"taskName": taskName, "taskType": taskType, "vesselName": "杨敏馨测试1",
                "vesselId": "63", "voyage": "SOS",
                "portName": "Shanghai Port", "terminalName": "军工路码头", "customer": "顾鹏",
                "expectStartTime": str(nowTimeStamp) + a, "expectEndTime": str(timeStamp) + a,
                "expectBerthTime": str(nowTimeStamp) + a, "expectDepartureTime": str(timeStamp) + a,
                "description": "任务描述"}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
        if taskType == '1' and r.json()['msg'] == '成功':
            print('创建打尺任务成功')
            taskId = r.json()['data']['taskId']
            return taskId
        elif taskType == '2' and r.json()['msg'] == '成功':
            print("创建监装任务成功")
            taskId = r.json()['data']['taskId']
            return taskId
        elif taskType == '3' and r.json()['msg'] == '成功':
            print("创建监卸任务成功")
            taskId = r.json()['data']['taskId']
            return taskId
        elif taskType == '5' and r.json()['msg'] == '成功':
            print("创建集港任务成功")
            taskId = r.json()['data']['taskId']
            return taskId

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
            print("文件上传失败：{}".format(r.json()))

    def get_plId(self, taskType, taskId):
        """
        根据任务类型，任务ID获取Pl信息
        """
        if taskType == '5':
            url = self.ip + '/api/cgi/listPl'
            headers = self.headers
            data = {
                'taskId': taskId
            }
            r = requests.get(url, headers=headers, params=data)
            if r.json()['msg'] == '成功':
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                plId = r.json()['data'][0]['plId']
                # 将Int型转换为str型
                return str(plId)
            else:
                print('获取plId失败：{}'.format(r.json()))
        elif taskType == '1':
            url = self.ip + '/api/mms/listPl'
            headers = self.headers
            data = {
                'taskId': taskId
            }
            r = requests.get(url, headers=headers, params=data)
            if r.json()['msg'] == '成功':
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                plId = r.json()['data'][0]['plId']
                # 将Int型转换为str型
                return str(plId)
            else:
                print('获取plId失败：{}'.format(r.json()))
        elif taskType == '2':
            url = self.ip + '/task/lps/listPl'
            headers = self.headers
            data = {
                'taskId': taskId,
                'taskType': taskType
            }
            r = requests.get(url, headers=headers, params=data)
            if r.json()['msg'] == '成功':
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                plId = r.json()['data'][0]['plId']
                # 将Int型转换为str型
                return str(plId)
            else:
                print('获取plId失败：{}'.format(r.json()))
        elif taskType == '3':
            url = self.ip + '/api/vds/listPl'
            headers = self.headers
            data = {
                'taskId': taskId,
                'taskType': taskType
            }
            r = requests.get(url, headers=headers, params=data)
            if r.json()['msg'] == '成功':
                print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
                plId = r.json()['data'][0]['plId']
                # 将Int型转换为str型
                return str(plId)
            else:
                print('获取plId失败：{}'.format(r.json()))


