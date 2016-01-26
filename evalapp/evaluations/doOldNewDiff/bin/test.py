#coding:utf-8
#!/usr/bin/python
import json
import os,sys

if __name__=="__main__":
	name_string="{\"weijianhao\":1}"
	name=json.dumps(name_string)
	print type(name)
	print name
	name_dict=json.loads(name)
	print type(name_dict)
	print name_dict["weijianhao"]
