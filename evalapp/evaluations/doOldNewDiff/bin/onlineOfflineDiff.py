#coding:utf-8
#!/usr/bin/python

from TestSite.module.online_offline_diff.src.GetPage import GetPage
from TestSite.module.online_offline_diff.src.Cmp import Cmp

def onlineOfflineDiff(param={}):
    result={"ret_code":0}
    try:
        #1：获取参数
        try:
            assert param.has_key("queryFile")
            queryFile=param["queryFile"]
        except Exception,e:
            result["ret_code"]=1
            return result
        
        #2：下载queryFile
        try:
            pass
        except Exception,e:
            result["ret_code"]=2
            return result

        #3：遍历queryFile发送请求
        try:
            pass
        except Exception,e:
            result["ret_code"]=3
            return result

        #4：保存结果
        try:
            pass
        except Exception,e:
            result["ret_code"]=3
            return result
        return result

    except Exception,e:
        result["ret_code"]=5
        return result
