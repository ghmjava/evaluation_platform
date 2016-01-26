"""evaluationPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', include('evalapp.urls')),
    url(r'^envbuild', views.envbuild, name='envbuild'),
    #url(r'^evaluate', views.evaluate, name='evaluate'),
    url(r'^evaluate_normeval', views.evaluate_normeval, name='evaluate_normeval'),
    url(r'^functiontest', views.functiontest, name='function_test'),
    url(r'^reportprocess', views.reportprocess, name='report_process'),
    #------------------jianhaowei create-----------------------
    url(r'^evaluate_online_offline_diff_input',views.evaluate_online_offline_diff_input, name='evaluate_online_offline_diff_input'),
    url(r'^evaluate_online_offline_diff_result',views.evaluate_online_offline_diff_result, name='evaluate_online_offline_diff_result'),
    #------------------hongmingguo create----------------------------------------
    url(r'^disk/', 'disk.views.register'),
    url(r'^up_file','disk.views.upload_tomcat_config_file'),
    url(r'^searchfile','disk.views.searchfile'),
]
