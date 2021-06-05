from pprint import pprint

from common.save_json import SaveJson

s = SaveJson().read_loading('timeLog')
print(type(s))
print(type(s[0]))
for i in s:
    if i['dataType']==1 or i['dataType']==2 or i['dataType']==7 or i['dataType']==8:
        print(i)
