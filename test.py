from pprint import pprint
from common.get_common import GetCommon
g = GetCommon()
detailInfo = g.get_detailInfo(taskId='1436', taskType='1')

pprint(detailInfo.json)
