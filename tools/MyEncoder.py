import json


# dumps是将dict数据转化为str数据，但是dict数据中包含byte数据所以会报错
class MyEncoder(json.JSONEncoder):
    """
    解码类 遇到byte就转为str
    """
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
