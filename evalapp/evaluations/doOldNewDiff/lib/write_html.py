#!/usr/bin/env python
#coding:utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf8')
def write_html(request_count, result, param, result_file, file_name):
    #create a html file
    file_path="/home/work/xusiwei/projects/evaluationPlatform/evalapp/templates/evalapp/tmpResult/%s.html"%(file_name)
    os.popen("touch %s"%(file_path))

    fp=open(file_path, 'a')
    os.popen("cat /dev/null > %s"%(file_path))

    #total
    fp.write("<!DOCTYPE html><html><head><meta http-equiv=\"Content Type\" content=\"text/html\" charset=\"utf-8\" /> <style>#container{margin-left: 20%;width:60%;margin-top: 50px;box-shadow: 10px 10px 5px #888888;} #content{text-align: center;background-color: rgb(101,147,74);} body {background-color: rgb(64,116,52);}</style></head><body><div id=\"container\"><div id=\"content\"><table height=\"100px\" width=\"600px\" align=\"center\"><caption align=\"top\">结果信息</caption><tr>")
    result_count=result[0]
    show_num_count=result[1]
    tids_count=result[2]
    
    result_percent=(0.0+request_count-show_num_count)/request_count
    show_num_percent=(0.0+request_count-tids_count)/request_count
    tids_percent=(0.0+request_count-tids_count)/request_count

    fp.write("<td>总不同：%.2f</td><td>tids不同：%.2f</td><td>show_num不同：%.2f</td>.</tr><tr>"%(result_percent,show_num_percent,tids_percent))
    fp.write("<td>请求总数：%d</td><td>tids相同数：%d</td><td>show_num相同数：%d</td>"%(request_count,show_num_count,tids_count))

    fp.write("</tr></table></div></div><div id=\"container\"><div id=\"content\"><table height=\"100px\" width=\"600px\" align=\"center\"><caption align=\"top\">详细信息</caption>")
    fp.write("<tr><td>所有参数是否相同</td><td>shows_num是否相同</td><td>tids是否相同</td><td>query</td></tr>")
    #deail_info
    data=open(result_file,'r')
    lines=data.readlines()
    for line in lines:
        line_set=line.split("\t")
        if line_set[0]=="1":
    	    fp.write("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(line_set[0],line_set[1],line_set[2],line_set[3]))
        else:
            fp.write("<tr bgcolor=#ff0000><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(line_set[0],line_set[1],line_set[2],line_set[3]))

    fp.write("</table></div></div></body></html>")

    data.close()
    fp.close()
