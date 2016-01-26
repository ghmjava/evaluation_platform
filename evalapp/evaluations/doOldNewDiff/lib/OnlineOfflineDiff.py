#coding:utf-8
#!usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import string
import copy
import time,datetime
from GetPage import GetPage
from Cmp import Cmp
from write_html import write_html

#从数据库读取query
sys.path.append("/home/work/xusiwei/projects/evaluationPlatform/evalapp")
from evalapp.generals.db import *
#from ReadExcel import ReadExcel
class OnlineOfflineDiff:
    #纪录线上url，线下url，纪录默认参数，纪录默认header，纪录请求参数文件位置，纪录请求参数比较文件位置
    def __init__(self,online_url,offline_url,param_dict,header_dict,request_file,param_file,result_file_name,is_more_info,queryNum,queryFile):
        self.online_url=online_url
        self.offline_url=offline_url
        self.param_dict=copy.deepcopy(param_dict)
        self.header_dict=copy.deepcopy(header_dict)
        self.request_file=request_file
        self.param_file=param_file
        self.param=[]
        self.result=[0]
        self.param_count=0
        self.request_count=0
        self.file_name=result_file_name
        self.result_file="/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/result/%s"%(result_file_name)
        self.is_more_info=is_more_info
        self.queryNum=queryNum
        self.queryFile=queryFile
    def start(self):
        #清空结果文件
        os.popen("cat /dev/null>%s"%(self.result_file))
        #定义一个线上请求GetPage
        online_getpage=GetPage(self.online_url,self.param_dict,self.header_dict)
        #定义一个线下请求GetPage
        offline_getpage=GetPage(self.offline_url,self.param_dict,self.header_dict)
        #将要比较的参数 去除\n 并读取数组中 初始化结果数组（第一个表示所有请求不同个数，其他分别表示比较参数不同个数）
        
        fp_param=self.param_file.split("&")
        for line in fp_param:
            self.param.append(line)
            self.result.append(0)
            self.param_count+=1
        
        #读取请求参数文件
        if self.queryNum == "":
            fp_request=open(self.request_file)
            #按行读取请求文件直到为空
            for line in fp_request:
                #去掉换行符
                line=line.strip("\n")
                #构造请求参数
                param={"query":'["%s"]'%(line)}
                #发送请求
                online_content=online_getpage.getpage(param)
                offline_content=offline_getpage.getpage(param)
    
                #比较请求结果,将本次比较的结果累加到最终结果里
                obj=Cmp(online_content,offline_content,self.param,self.result_file,line,self.is_more_info)
                result=obj.start()
                for i in range(self.param_count+1):
                    self.result[i]+=result[i]
                #将请求总数＋1
                self.request_count=self.request_count+1
            fp_request.close()
        else:
            requst_query=getquerylist(datetime.date.today(),2,int(self.queryNum))
            #按行读取请求文件直到为空
            for line in requst_query:
                #构造请求参数
                param={"query":'["%s"]'%(line["key_name"])}
                #发送请求
                online_content=online_getpage.getpage(param)
                offline_content=offline_getpage.getpage(param)
    
                #比较请求结果,将本次比较的结果累加到最终结果里
                obj=Cmp(online_content,offline_content,self.param,self.result_file,line["key_name"],self.is_more_info)
                result=obj.start()
                for i in range(self.param_count+1):
                    self.result[i]+=result[i]
                #将请求总数＋1
                self.request_count=self.request_count+1 
        #打印结果
        write_html(self.request_count,self.result,self.param,self.result_file, self.file_name)
        print "请求总数%s"%(self.request_count)
        for i in range(self.param_count+1):
            if i==0:
                print "请求总相同数:%d "%(self.result[0])
            else:
                print "参数%s总相同总数:%d "%(self.param[i-1],self.result[i])
