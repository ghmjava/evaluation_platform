#coding;utf-8
#!/usr/bin/python

import time
import sys,os

def createFileByTime(filePath=""):
	fileName=""
	if filePath=="":
		return fileName
	else:
		try:
			#get current time
			fileName=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
			os.popen("touch %s/%s"%(filePath,fileName))
			return fileName
		except Exception,e:
			return fileName

	
