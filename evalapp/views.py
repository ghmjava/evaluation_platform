from django.shortcuts import render

from common import *
from .models import *

from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
# Create your views here.

def envbuild(request):
    pass

def evaluate_normeval(request):
    from evaluations.doNormalEvaluation import analyzer
    page_url = ''
    if "page_url_prefix" in request.GET:
        page_url_prefix = request.GET['page_url_prefix']
    evalHandler = analyzer.PosterMonitorHanlder(page_url_prefix)
    htmlPage = evalHandler.get()
    print htmlPage
    return HttpResponse(htmlPage)

'''
def evaluate(request):
    #jianhaowei create
    result={"ret_code":0}
    from evaluations import *
    if request.method == "POST":
        paramDict=request.POST.dict()

        if paramDict.has_key("doNormalEvaluation") and paramDict['doNormalEvaluation'] == 'true':
            pass

        if paramDict.has_key("doHttpThriftDiff") and paramDict['doHttpThriftDiff'] == 'true':
            pass

        if paramDict.has_key("doOldNewDiff") and paramDict['doOldNewDiff'] == 'true':
            from doOldNewDiff.bin.onlineOfflineDiff import onlineOfflineDiff
            result=onlineOfflineDiff(paramDict)
    else:
        paramDict=request.GET.dict()
        if paramDict.has_key("doOldNewDiff") and paramDict['doOldNewDiff'] == 'true':
            return render_to_response('doOnlineOfflineDiffData.html')        

    return HttpResponse(json.dumps(result),content_type="application/json")
'''

def functiontest(request):
    pass

def reportprocess(request):
    pass

#jianhaowei create
def evaluate_online_offline_diff_input(request):
    #jianhaowei create
    result={"ret_code":0}
    from evaluations import *
    if request.method == "POST":
        paramDict=request.POST.dict()
        if paramDict.has_key("doOldNewDiff") and paramDict['doOldNewDiff'] == 'true':
            from doOldNewDiff.bin.onlineOfflineDiff import onlineOfflineDiff
            result=onlineOfflineDiff(paramDict)
    else:
        paramDict=request.GET.dict()
        if paramDict.has_key("doOldNewDiff") and paramDict['doOldNewDiff'] == 'true':
            return render_to_response('doOnlineOfflineDiffData.html')        

    return HttpResponse(json.dumps(result),content_type="application/json")    

def evaluate_online_offline_diff_result(request):
    from  evaluations.doOldNewDiff.lib.OnlineOfflineDiff import OnlineOfflineDiff
    from  evaluations.doOldNewDiff.lib.createFileByTime import createFileByTime

    if "online_url" in request.GET:
        #create different file for different user
        file_name=createFileByTime("/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/result")
        if file_name=="":
            assert 0==1
        
        online_url=request.GET['online_url']
        offline_url=request.GET['offline_url']
        show_num=request.GET['show_num']
        tids=request.GET['tids']
        queryNum=request.GET['queryNum']
        queryFile=request.GET['queryFile']
        
        compare_param="show_num"+"\t"+show_num+"&"+"tids"+"\t"+tids
        obj=OnlineOfflineDiff(online_url,offline_url,{"offset":0,"limit":960,"query":'[" "]',"platform":"web", "sort":'boom', "debug":0, "close_cache":1, }, {'Meilishuo':'uid:9;ip:111.206.87.114;v:1;master:0'},"/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/data/%s"%(queryFile), compare_param,file_name, 0,queryNum,queryFile)
        
        obj.start()
        return render_to_response('%s.html'%(obj.file_name))
