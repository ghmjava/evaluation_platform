#coding:utf-8
#!usr/bin/python
import urllib
import urllib2
import copy
class GetPage:
	#初始化函数，纪录url，默认参数，header
	def __init__(self,page_url,param_dict={},header_dict={}):
		self.page_url=page_url
		self.param_dict=param_dict
		self.header_dict=header_dict
	#需要传递参数字典
	def getpage(self,param_dict):
		#添加新的参数到默认参数字典中，或者改变默认参数的值
		for key in param_dict:
			if param_dict.has_key(key):
				self.param_dict[key]=param_dict[key]
		#将参数字典转变成 参数＝值&参数＝值&....形式
		param=urllib.urlencode(self.param_dict)
		#拼接请求
		req=urllib2.Request(self.page_url,param,self.header_dict)
		#发送请求
		response=urllib2.urlopen(req)
		#读取返还值，返还一个json格式数据
		page=response.read()
		return page
