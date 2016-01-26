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
    fp.write("<html>")
    fp.write("<head>")
    fp.write("<title>Result</title>")
    fp.write("<head>") 
    fp.write("<body>") 
    #total
    fp.write("<h2>")
    fp.write("request_total：%d &nbsp &nbsp &nbsp"%request_count)
    fp.write("result_total：%d"%result[0])
    fp.write("<p/>")
    i=1 
    for param_name in param:
        fp.write("%s：%d &nbsp &nbsp &nbsp"%(param_name,result[i]))
        i=i+1
        fp.write("<p/>")
    fp.write("</h2>")

    #deail_info
    data=open(result_file,'r')
    fp.write("<table>") 
    lines=data.readlines()
    for line in lines:
    	fp.write("<tr>")
       	fp.write("<td>")
        fp.write(line)
        fp.write("</td>")
        fp.write("</tr>")
    fp.write("</table>")
    fp.write("<body>")  
    fp.write("</html>")

    data.close()
    fp.close()
