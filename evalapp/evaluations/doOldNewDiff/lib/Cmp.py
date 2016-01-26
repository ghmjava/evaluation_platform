#coding:utf-8
#!usr/bin/python
import json
import os
class Cmp:
    def __init__(self,online,offline,param_dict,result_file,query,is_more_info):
        self.online=online
        self.offline=0
        if offline != None:
            self.offline = offline
        else:
            print "Error happened for QUERY ", query 
        self.param=param_dict
        self.result=[1]
        self.param_count=len(self.param)
        self.result_file=result_file
        self.query=query
        self.is_more_info=is_more_info

    def start(self):
        for i in range(self.param_count):
            ret=1
            #将比较参数，和限制条件读取出来
            line=self.param[i]
            line_set=line.split("\t")
            param_name=line_set[0]
            param_limit=float(line_set[1])

            #根据比较参数不同，调用相应的比较函数
            if param_name=="show_num":
                ret=self.cmp_show_num(param_limit)
            elif param_name=="tids":
                ret=self.cmp_tids(param_limit)
            #纪录参数比较结果
            self.result.append(ret)
            #纪录本次比较结果是否相同
            if ret==0:
                self.result[0]=0
        #将本次对比结果写入到result_file文件
        line=""
        for i in self.result:
            line=line+str(i)+"\t"
        line =line[:-1]
        print line+"\t"+self.query
        fp_result=open(self.result_file,'a')
        fp_result.write(line+"\t"+self.query+"\n")
        fp_result.close()

        #返回本次比较结果
        return self.result

#*********下面是比较函数，如果相同则返还0，不同返还1***************************************************************
    def cmp_show_num(self,limit):
        online_dict=json.loads(self.online)
        offline_dict=json.loads(self.offline)
        #比较show_num是否相同
        online_num=online_dict['data']['show_num']
        offline_num=offline_dict['data']['show_num']
        
        if self.is_more_info!=0:
            print online_num
            print offline_num
        if offline_num==0:
            if online_num==0:
                print "商品数都为0"
                return True
            else:
                print "旧版商品数为0"
                return False
        else:
            value = 1
            try:
                value=abs(online_num-offline_num)/(offline_num+0.0)
            except:
                print "DEBUG query: ", self.query
                print "DEBUG ONLINE NUM: ", online_num
                print "DEBUG OFFLINE NUM: ", offline_num
            if self.is_more_info==0:
                print value
            return     value < limit
        
    def cmp_tids(self,limit):
        online_dict=json.loads(self.online)
        offline_dict=json.loads(self.offline)
        #比较tids是否相同
        online_data=online_dict['data']['tids']
        offline_data=offline_dict['data']['tids']
        if offline_data is None:
            print "No tids for QUERY ", self.query
            offline_data = []
        n=0
        for i in online_data:
            if i not in offline_data:
                n=n+1
        if self.is_more_info!=0:
            print online_data
            print offline_data
        if len(offline_data)==0:
            if len(online_data)==0:
                print "商品tids数都为0"
                return True
            else:
                print "旧版商品tids数为0"
                return False
        else:
            if self.is_more_info==0:
                print n/(len(offline_data)+0.0)
            return n/(len(offline_data)+0.0) < limit
    
