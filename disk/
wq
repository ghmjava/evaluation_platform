#coding=utf-8
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect 
from disk.models import User

from django.template import RequestContext 
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.csrf import csrf_protect 
import os

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()
    
def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
            #写入数据库
            user = User()
            user.username = username
            user.headImg = headImg
            user.save()
            #查询数据库
            files=os.listdir('/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/data/')
            lines=''
            for filename in files: 
                    lines=lines+filename+"<br/>"        
            return HttpResponse(lines)
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})



#上传文件 
@csrf_exempt 
@csrf_protect 
def upload_tomcat_config_file(request): 
    from django import forms 
    class UploadFileForm(forms.Form): 
        title = forms.CharField(max_length=1000000) 
        file = forms.FileField() 
    if request.method == "GET": 
        data='get'
    if request.method == "POST": 
        f = handle_uploaded_file(request.FILES['t_file'])
        #files=os.listdir('/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/data/')
        #lines=''
        #for filename in files:
        #    lines=lines+filename+"<br/>"
        #return HttpResponse(lines) 
    return render_to_response('upload_config_file.html',context_instance=RequestContext(request)) 
    #return HttpResponse(data) 
def handle_uploaded_file(f): 
    f_path='/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/data/'+f.name 
    with open(f_path, 'wb+') as info: 
        print f.name 
        for chunk in f.chunks(): 
            info.write(chunk) 
    return f 
#上传文件结束
#def searchfile()
#    for filename in os.listdir(r'/home/work/xusiwei/projects/evaluationPlatform/upload'):
#        return HttpResponse(filename)



def searchfile(request):
    # if this is a POST request we need to process the form data
        if request.method == 'POST':
        #create a form instance and populate it with data from the request
        #check whether it's valid:
            files = os.listdir('/home/work/xusiwei/projects/evaluationPlatform/evalapp/evaluations/doOldNewDiff/data/')
            lines=''
            for filename in files:
                lines=lines+filename+"<br/>"
            return HttpResponse(lines)
        # if a GET (or any other method) we'll create a blank form
        else:
            return HttpResponse("upload OK!")
