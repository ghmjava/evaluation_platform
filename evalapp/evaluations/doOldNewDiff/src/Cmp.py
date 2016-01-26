#coding:utf-8
#!/usr/bin/python
import json

class Cmp:
	def __init__(online_data,offline_data):
		self.online_data=online_data
		self.offline_data=offline_data
	def cmp():
		error_result={"ret_code":1}

		try:
			result={"ret_code":0}
			#讲json数据转换成字典
			online_dict=json.loads(self.online_data)
			offline_dict=json.loads(self.offline_data)
			
			#记录show_num
			result["online_show_num"]=online_dict['data']['show_num']
			result["offline_show_num"]=offline_dict['data']['show_num']
			
			#记录tids
			if 'tids' in online_dict['data']:
				result["online_tids_num"]=len(online_dict['data']['tids'])
			else:
				result["online_tids_num"]=0
			if 'tids' in offline_dict['data']:
				result["offline_tids_num"]=len(offline_dict['data']['tids'])
			else:
				result["offline_tids_num"]=0

			#返还结果
			return result
			
		except Exception,e:
			return error_result
