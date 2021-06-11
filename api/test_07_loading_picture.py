import datetime
import json
import time
import warnings
import requests
import unittest
from common.get_common import GetCommon
from common.read_ini import ReadIni
from common.save_json import SaveJson


class TestLoadingPicture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        cls.r = ReadIni()
        cls.g = GetCommon()
        cls.s = SaveJson()
        # 获取环境
        cls.ip = cls.r.get_ip()
        # 设置任务类型
        cls.taskType = '2'
        # 设置登录的类型
        cls.os = cls.r.get_os()
        # 获取token
        cls.token = cls.r.get_token()
        # 设置请求头
        cls.headers = {
            'os': cls.os,
            'Authorization': cls.token,
            'versionName': '1.6.11'
        }
        # 装前货况图片路径
        cls.beforeLoadingPath = cls.r.get_loading_picture_path('beforeLoadingPath')
        # 船舶概况图片路径
        cls.shipSurveyPath = cls.r.get_loading_picture_path('shipSurveyPath')
        # 装载过程图片路径
        cls.eventNodePath = cls.r.get_loading_picture_path('eventNodePath')
        # 绑扎材料照片路径
        cls.materialPath = cls.r.get_loading_picture_path('materialPath')
        # OSS路径
        cls.ossPath = cls.r.get_oss_path()

    @classmethod
    def tearDown(cls) -> None:
        pass

    @staticmethod
    def outPut(url, data=None, r=None):
        return "请求：{} \n数据：{}\n返回：{} ".format(url, data, r.json())

    def test_01_set_before_loading(self):
        """
        装前货况上传其他类型照片
        """
        global taskId
        # 获取taskId
        taskInfo = self.s.read_loading('addTask')
        taskId = taskInfo['taskId']
        url = self.ip + '/task/lps/setBeforeLoading'
        headers = self.headers
        data = [
            {
                "abnormal": 17,
                "dataType": '1',  # 1.场地整体数据 2.BL整体数据 3.单件数据
                "mediaType": '1',  # 媒体类型1：照片3：视频
                "path": self.beforeLoadingPath,
                "tag": "其他照片标签",  # 照片标签
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_02_set_before_loading(self):
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
                "path": self.beforeLoadingPath,
                "plId": plId,  # plID
                "tag": "BL整体照片标签",  # 照片标签
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_03_set_before_loading(self, number=0):
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
                "path": self.beforeLoadingPath,
                "plDetailId": plDetailId,
                "plId": plId,
                "tag": "明细照片标签",
                "taskId": taskId,
            }
        ]

        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_04_set_shipSurvey(self):
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
                "path": self.shipSurveyPath,  # 照片路径
                "tag": "船舶整体照片标签",
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_05_set_shipSurvey(self):
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
                "path": self.shipSurveyPath,
                "spaceId": spaceId,  # 舱位id
                "spaceName": spaceName,
                "tag": "舱位照片标签",
                "taskId": taskId,
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_06_set_eventNode(self):
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
                "path": self.eventNodePath,
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

    def test_07_set_eventNode(self):
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
                "path": self.eventNodePath,
                "plId": plId,
                "tag": "BL整体照片标签",
                "taskId": taskId,
                "timeStamp": str(nowTimeStamp) + '000'
            }
        ]
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(self.outPut(url, data, r))
        self.assertEqual(r.json()['msg'], '成功')

    def test_08_set_eventNode(self):
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
                "path": self.eventNodePath,
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

    def test_09_list_vls_materials(self):
        """
        获取系统内全部绑扎材料基础数据并写入JSON文件
        """
        url = self.ip + '/task/vls/listVlsMaterials'
        headers = self.headers
        r = requests.get(url, headers=headers)
        print(self.outPut(url, r=r))
        self.assertEqual(r.json()['msg'], '成功')
        # 写入JSON文件
        self.s.write_loading('materals', r.json()['data'])

    # @unittest.skip("跳过")
    def test_10_set_vls_material_data(self):
        """
        上传绑扎材料照片
        """
        url = self.ip + '/task/vls/setVlsMaterialData'
        headers = self.headers
        materalsInfo = self.s.read_loading('materals')
        lashingMaterialInfo = self.s.read_loading('LashingMaterial')
        for materals in materalsInfo:
            for lashingMaterial in lashingMaterialInfo:
                if materals['id'] == int(lashingMaterial['materialId']):
                    materialId = materals['id']
                    materialName = materals['materialName']
                    materialType = materals['materialType']
                    norms = lashingMaterial['norms']
                    data = [
                        {
                            "imageRemark": "绑扎照片备注",
                            "materialId": materialId,  # 材料ID
                            "materialName": materialName,  # 材料名称
                            "materialType": materialType,  # 材料类型
                            "mediaType": 1,  # 媒体类型 1：照片 3：视频
                            "norms": norms,  # 规格
                            "path": self.materialPath,  # 照片路径
                            "unite": "立方米（m³）",  # 单位
                            'taskId': taskId,
                            "url": self.ossPath+self.materialPath
                            # 照片URL
                        }
                    ]

                    r = requests.post(url, headers=headers, data=json.dumps(data))
                    print(self.outPut(url, data, r))
