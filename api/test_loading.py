import datetime
import time
import unittest
import warnings
import requests
import json

from parameterized import parameterized

from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        r = ReadIni()
        cls.g = GetCommon()
        cls.s = SaveJson()
        # 获取环境
        cls.ip = r.get_ip()
        # 设置任务类型
        cls.taskType = '2'
        # 设置登录的类型
        cls.os = r.get_os()
        # 获取token
        cls.token = r.get_token()
        # 设置请求头
        cls.headers = {
            'os': cls.os,
            'Authorization': cls.token
        }

    @classmethod
    def tearDownClass(cls) -> None:
        """
        从数据库中删除任务
        """

    @staticmethod
    def outPut(url, data, r):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    @parameterized.expand([('杨敏馨测试1', 'Sos', 'Shanghai Port', '军工路码头', '任务描述', '顾鹏')])
    def test_01_add_task(self, vesselName, voyage, portName, terminalName, description, customer):
        """
        添加任务并将任务信息写入文件
        """
        global taskName
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        threeDayAgo = (datetime.datetime.now() + datetime.timedelta(days=7))
        # 获取7天后的时间戳
        timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        a = '000'
        url = self.ip + '/task/index/addTask'
        headers = self.headers
        if self.os == '1':
            taskName = '安卓/监装'
        elif self.os == '2':
            taskName = 'IOS/监装'
        data = {"taskName": taskName, "taskType": self.taskType, "vesselName": vesselName,
                "vesselId": self.g.get_vessel_Id(vesselName), "voyage": voyage, "portName": portName,
                "terminalName": terminalName, "customer": customer, "expectStartTime": str(nowTimeStamp) + a,
                "expectEndTime": str(timeStamp) + a, "expectBerthTime": str(nowTimeStamp) + a,
                "expectDepartureTime": str(timeStamp) + a, "description": description}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        # response
        self.outPut(url, data, r)
        msg = r.json()['msg']
        self.assertEqual(msg, '成功')
        # 将请求返回数据写入JSON文件
        self.s.write_loading('addTask', r.json()['data'])

    def test_02_import_pl(self, fileName='标准模板'):
        """
        验证监装任务--模板导入
        """
        global taskId
        # 获取plId
        taskInfo = self.s.read_loading('addTask')
        taskId = taskInfo['taskId']
        pathKey = self.g.check_pl(taskId, self.taskType, fileName=fileName)
        if pathKey:
            url = self.ip + '/task/lps/createPl'
            data = {"taskId": taskId, "shippingOrder": "清单1", "lengthUnit": 2, "weightUnit": 1,
                    "pathKey": pathKey}
            headers = self.headers
            r = requests.post(url, data=json.dumps(data), headers=headers)
            print("请求：{} \ndata:{} \n返回：{} ".format(url, data, r.json()))
            msg = r.json()['msg']
            self.assertEqual(msg, '成功')

    def test_03_start_task(self):
        """
        开始任务
        """
        url = self.ip + '/task/index/startTask'
        headers = self.headers
        data = {
            'taskId': taskId,
            'taskType': self.taskType
        }
        r = requests.get(url, headers=headers, params=data)
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_04_add_group(self):
        """
        创建工班
        """
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        threeDayAgo = (datetime.datetime.now() + datetime.timedelta(days=7))
        # 获取7天后的时间戳
        timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        url = self.ip + '/task/lps/addGroup'
        headers = self.headers
        data = {
            "description": "白日依山尽，黄河入海流，欲穷千里目，更上一层楼",
            "groupEndTime": str(timeStamp) + '000',
            "groupName": "工班 1-1-1",
            "groupStartTime": str(nowTimeStamp) + '000',
            "taskId": taskId
        }
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')
        # 将创建的工班信息写入JSON文件
        self.s.write_loading('group', r.json()['data'])

    def test_05_set_before_loading(self):
        """
        装前货况上传其他类型照片
        """
        url = self.ip + '/task/lps/setBeforeLoading'
        headers = self.headers
        data = [
            {
                "abnormal": 17,
                "dataType": '1',  # 1.场地整体数据 2.BL整体数据 3.单件数据
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "tag": "其他照片标签",  # 照片标签
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_06_set_before_loading(self):
        """
        装前货况上传BL整体照片
        """
        global plId
        # 获取PL信息
        plInfo = self.g.get_plInfo(taskId, self.taskType)
        plId = plInfo[0]['plId']
        url = self.ip + '/task/lps/setBeforeLoading'
        headers = self.headers
        data = [
            {
                "abnormal": '17',
                "dataType": '2',  # 1.场地整体数据 2.BL整体数据 3.单件数据
                "imageRemark": "照片备注",
                "mediaType": '1',
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "plId": plId,  # plID
                "tag": "BL整体照片标签",  # 照片标签
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_07_set_before_loading(self, number=0):
        """
        装前货况上传明细照片
        """
        global plDetailId
        # 获取明细信息
        detailInfo = self.g.get_detailInfo(taskId, self.taskType)
        plDetailId = detailInfo[number]['plDetailId']
        url = self.ip + '/task/lps/setBeforeLoading'
        headers = self.headers
        data = [
            {
                "abnormal": '17',
                "dataType": '3',  # 1.场地整体数据 2.BL整体数据 3.单件数据
                "imageRemark": "照片备注",
                "mediaType": '1',
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "plDetailId": plDetailId,
                "plId": plId,
                "tag": "明细照片标签",
                "taskId": taskId,
            }
        ]

        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_08_set_shipSurvey(self):
        """
        船舶概况上传船舶整体照片
        """
        global vesselId
        # 获取监装船舶ID
        vesselId = self.s.read_loading('addTask')['vesselId']
        url = self.ip + '/task/lps/setShipSurvey'
        headers = self.headers
        data = [
            {
                "abnormal": '17',
                "dataType": '1',  # 数据类型1.船舶整体数据3.舱位数据
                'dataId': vesselId,  # 监装船舶数据Id
                "imageRemark": "船舶整体照片备注",
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",  # 照片路径
                "tag": "船舶整体照片标签",
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_09_set_shipSurvey(self):
        """
        船舶概况上传舱口舱位照片
        """
        global hatchId, hatchName, spaceId, spaceName
        url = self.ip + '/task/lps/setShipSurvey'
        headers = self.headers
        # 获取NO.I舱口ID/Name
        hatches = self.g.get_hatches(vesselId)
        hatchId = hatches[0]['hatchId']
        hatchName = hatches[0]['hatchName']
        # 获取舱位信息
        spaces = self.g.get_spaces(vesselId)
        spaceId = spaces[0]['spaceId']
        spaceName = spaces[0]['spaceName']
        data = [
            {
                "abnormal": '17',
                "dataId": vesselId,  # 监装船舶数据Id
                "dataType": '3',  # 数据类型1.船舶整体数据3.舱位数据
                "hatchId": hatchId,  # 舱口ID
                "hatchName": hatchName,
                "imageRemark": "舱位照片备注",
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "spaceId": spaceId,  # 舱位id
                "spaceName": spaceName,
                "tag": "舱位照片标签",
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_10_set_eventNode(self):
        """
        装载过程上传舱位整体照片
        """
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        url = self.ip + '/task/lps/setEventNode'
        headers = self.headers
        data = [
            {
                "abnormal": '17',  # 异常
                "dataId": vesselId,  # 监装过程数据Id
                "dataType": '1',  # 数据类型 1.舱位整体照片 2.BL整体照片 3.单件照片
                "hatchId": hatchId,  # 舱口ID
                "hatchName": hatchName,
                "imageRemark": "舱位整体照片备注",  # 照片备注
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "spaceId": spaceId,  # 舱位id
                "spaceName": spaceName,
                "tag": "舱位整体照片标签",
                "taskId": taskId,
                "timeStamp": str(nowTimeStamp) + '000'
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_11_set_eventNode(self):
        """
        装载过程上传BL整体照片
        """
        url = self.ip + '/task/lps/setEventNode'
        headers = self.headers
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        data = [
            {
                "abnormal": '17',  # 异常
                "dataType": '2',  # 数据类型 1.舱位整体照片 2.BL整体照片 3.单件照片
                "imageRemark": "BL整体照片备注",  # 照片备注
                "lashingFlag": '1',  # 是否为绑扎照片0:否 1:是
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "plId": plId,
                "tag": "BL整体照片标签",
                "taskId": taskId,
                "timeStamp": str(nowTimeStamp) + '000'
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_12_set_eventNode(self):
        """
        装载过程上传明细照片
        """
        url = self.ip + '/task/lps/setEventNode'
        headers = self.headers
        nowTime = datetime.datetime.now()
        # 获取当前时间戳
        nowTimeStamp = int(time.mktime(nowTime.timetuple()))
        data = [
            {
                "abnormal": '17',  # 异常
                "dataType": '3',  # 数据类型 1.舱位整体照片 2.BL整体照片 3.单件照片
                "imageRemark": "明细照片备注",  # 照片备注
                "lashingFlag": '1',  # 是否为绑扎照片0:否 1:是
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": "13/task/lps/96/goods/2020-09-29@14-20-31-70-44d9.jpg",
                "plDetailId": plDetailId,
                "plId": plId,
                "tag": "明细照片标签",
                "taskId": taskId,
                "timeStamp": str(nowTimeStamp) + '000'
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')