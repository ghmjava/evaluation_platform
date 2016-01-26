#!/usr/bin/env python
#coding:utf-8

import os, sys
import time, datetime
import simplejson as sj
from norm_count_tools import NormCountTools
sys.path.append("/home/work/xusiwei/projects/evaluationPlatform/evalapp")
from generals.db import *
from generals.networktools import *
import multiprocessing
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

class PosterMonitorHanlder():

    def __init__(self, page_url_prefix=''):
        #client信息
        self.header = {'Meilishuo':'uid:3855122;ip:182.16.0.18;v:1;master:0'}
        self.method = 'POST'
        #页面参数
        if page_url_prefix == '':
            self.page_url = 'http://virus.siweixu.qalab.meilishuo.com/goodslist/get_goods_list?debug=1'
        else:
            self.page_url = 'http://' + page_url_prefix + ".meilishuo.com/goodslist/get_goods_list?debug=1"
        print self.page_url
        self.page_num = 100
        self.page_start = 0
        self.page_limit = 160#320
        #self.page_limit = 320
        #self.page_limit = 500#320
        self.sort = 'weight'
        self.platform = 'mob'
        self.summarize = {}

    def processEval(self, page_url, post_data, header, key):
        json_res = reqPOST(page_url, post_data, header)
        self.summarize[key] = {160:self.summarizationOfData(json_res['data'], 160),
            40:self.summarizationOfData(json_res['data'], 40),}
        return

    def get(self):
        try:
            single_pid = self.get_argument('pid')
        except Exception as e:
            single_pid = False
        try:
            self.sort = self.get_argument('sort')
        except Exception as e:
            pass
        print >> sys.stderr,self.page_url
        start_time = time.time()
        #获取pid pv top 100
        #pids = []
        #if not single_pid:
        #    print "Use getPid!"
        #    pids = self.getPid(datetime.date.today() - datetime.timedelta(days=2))
        #else:
        #    pids = [int(single_pid)]
        #print >> sys.stderr,"%s"%(str(pids))

        #pids = [1645,1625,1607,1811,533,3131,1793,497,539,1559]
        #pids = [1605,425,439,4981,417,1235,2569,413,423,91153,531,3883,5337,747,545,1911,174379,2605,5701,535,433,5985,5697,138573,717,6165,749,727,3925,3595,1551,5911,477,459,415,1817,481,437,177121,178753,749,177197,735,3085,5679,6165,449,175369,178073,451]
        #pids = [19435]
        #print "DEBUG pids: ", pids
        #添加请求pages
        error = 'ERROR pid:'
        errorNum = 0
        count = 0
        #统计
        #summarize = {}
        #print >> sys.stderr,pids
        #if  response_platform == 'zxvirus':
        #  tmpParam = 'zxplat=test01&zxenv=test01'
        querys = self.getQuery(datetime.date.today())

        pool = ThreadPool(processes=multiprocessing.cpu_count())
        for query in querys:
            queryencoded = '["' + query.encode('utf-8') + '"]'
            print >> sys.stderr,'processing query is ', queryencoded
            post_data = {'query':queryencoded, 'offset':self.page_start, 'limit':self.page_limit, 'sort':self.sort, 'platform':self.platform,}
            print >> sys.stderr, post_data
            pool.apply_async(self.processEval, (self.page_url, post_data, self.header, query))
            #print summarize
            #print >> sys.stderr,'pid:'+str(pid)+'\tact:'+str(summarize[pid][160]['active_fill_rate'])
          #wsscwqx
            #summarize[pid] = {320:self.summarizationOfData(json.loads(response.body)['data'], 320)}
            count+=1
        pool.close()
        pool.join()
    
        end_time = time.time()
        use_time = end_time - start_time

        print '耗时:'+str(use_time)
        print str(errorNum)+error
        print 'all request:%d' % count

        total = self.sumData(self.summarize)
        print total
        showCode = self.dataToShow(total)
        showCodeWithSkin = self.getSkin(showCode)
        #showCodeWithSkin = self.getSkin(str(json.loads(response.body)['data']))
        #self.write(showCodeWithSkin)
        #self.finish()
        print showCodeWithSkin
        return showCodeWithSkin

    def getSkin(self, showCode):
        before = """<html lang="zh-cn" slick-uniqueid="3"><head>
                <link rel="stylesheet" href="http://cdn.bootcss.com/twitter-bootstrap/3.0.3/css/bootstrap.min.css">
                <meta charset="utf-8">
                <title>debug</title>
                <style type="text/css">
                ::selection{ background-color: #E13300; color: white; }
                ::moz-selection{ background-color: #E13300; color: white; }
                ::webkit-selection{ background-color: #E13300; color: white; }
                code {
                    font-family: Consolas, Monaco, Courier New, Courier, monospace;
                    font-size: 12px;
                    background-color: #f9f9f9;
                    border: 1px solid #D0D0D0;
                    color: #002166;
                    display: block;
                    margin: 8px 0 8px 0;
                    padding: 8px 8px 8px 8px;
                }
                body {
                    background-color: #fff;
                    margin: 40px;
                    font: 13px/20px normal Helvetica, Arial, sans-serif;
                    color: #4F5155;
                }
                #body{
                    margin: 0 15px 0 15px;
                }
                #container{
                    margin: 10px;
                    border: 1px solid #D0D0D0;
                    -webkit-box-shadow: 0 0 8px #D0D0D0;
                }
                td{
                    width:2px;
                }
                </style>
                <body style="">
                <div id="container">"""
        end = """ </div>
                </body>
                </html>"""
        return before + showCode + end

    def summarizationOfData(self, data, num):
        """
        将一个page的data汇总成想要的指标
        """
        #统计指标

        first_page = NormCountTools(data, num)
        stat = {
            'fashion_score':first_page.fashion_score(),
            'fashion_rate':first_page.fashion_rate(),
            'new_score':first_page.new_score(),
            'new_rate':first_page.new_rate(),
            'boom_score':first_page.boom_score(),
            'boom_rate':first_page.boom_rate(),
            'popular_score':first_page.popular_score(),
            'popular_rate':first_page.popular_rate(),
            #'health_degree':first_page.health_degree(),
            'bad_goods_rate':first_page.bad_goods_rate(),
            'acg_fill': first_page.acg_fill(),
            'pic_score_4':first_page.pic_score_rate_4(),
            'pic_score_3':first_page.pic_score_rate_3(),
            'style_score_4':first_page.style_score_rate_4(),
            'style_score_3':first_page.style_score_rate_3(),
            'ka_rate':first_page.ka_rate(),
            'price':first_page.price(),
            'shop_level_5':first_page.shoplevel(5),
            'shop_level_4':first_page.shoplevel(4),
            'shop_level_3':first_page.shoplevel(3),
            'shop_level_2':first_page.shoplevel(2),
            'shop_level_1':first_page.shoplevel(1),
            'shop_level_0':first_page.shoplevel(0),
            'area_n':first_page.area(2),
            'area_s':first_page.area(3),
            'area_e':first_page.area(1),
            'avg_ctr':first_page.avg_ctr(),
            'avg_dsr':first_page.avg_dsr(),
            'shop_service':first_page.shop_service(),
            'avg_reason_refund_rate':first_page.avg_reason_refund_rate(),
            'avg_appeal_rate':first_page.avg_appeal_rate(),
            'avg_intime_response_rate':first_page.avg_intime_response_rate(),
            'avg_first_response_time':first_page.avg_first_response_time(),
            'avg_express_rate':first_page.avg_express_rate(),
            'golden_fill_rate':first_page.golden_fill_rate(),
            'top_fill_rate':first_page.top_fill_rate(),
            'active_fill_rate':first_page.active_fill_rate(),
            'ecpm':first_page.ecpmscore()
            }
        return stat

    def sumData(self, summarize):
        sum = {40:{},160:{}}
        #sum = {160:{}}
        total = len(summarize)
        for query in summarize:
            for num in summarize[query]:
                for key in summarize[query][num]:
                  try:
                    sum[num][key] = sum[num].get(key, 0.0) + summarize[query][num][key]
                  except Exception as e:
                    print >> sys.stderr,"%s____%s___%s"%(e,key,str(summarize))
                    
        for num in sum:
            for key in sum[num]:
                sum[num][key] = round(sum[num][key]*1.0/total, 4)
        return sum

    def dataToShow(self, summarize):
        statNameMap = [
                        ['style_score_4','款式4分'],
                        ['style_score_3','款式3分'],
                        ['pic_score_4','图片4分'],
                        ['pic_score_3','图片3分'],
                        ['new_rate','新品率'],
                        ['new_score','平均上架时间'],
                        ['ecpm','ecpm'],
                        ['boom_score','平均热销分'],
                        ['boom_rate','热销商品占比'],
                        ['avg_ctr','平均ctr'],
                        ['ka_rate','ka填充'],
                        ['shop_level_5','5级商家占比'],
                        ['shop_level_4','4级商家占比'],
                        ['shop_level_3','3级商家占比'],
                        ['shop_level_2','2级商家占比'],
                        ['shop_level_1','1级商家占比'],
                        ['shop_level_0','0级商家占比'],
                        ['area_n','华北商家占比'],
                        ['area_s','华南商家占比'],
                        ['area_e','华东商家占比'],
                        ['acg_fill','推广商品填充率'],
                        ['avg_dsr','平均dsr'],
                        ['shop_service','花花在线率'],
                        ['avg_intime_response_rate', '花花及时回复率'],
                        ['avg_first_response_time', '花花首次响应时间'],
                        ['avg_express_rate','及时发货率'],
                        ['price','price'],
                        ['avg_reason_refund_rate', '有理由退款率'],
                        ['golden_fill_rate', '黄金橱窗填充率'],
                        ['top_fill_rate', '橱窗填充率'],
                        ['active_fill_rate', '520活动大促填充率'],
              ]
        pageNameMap = {40:'前两贞', 160:'第一页'}
        #pageNameMap = {160:'第一页'}
        code = '<div class="bs-example"> <table class="table table-hover">'
        for num in summarize:
            code += "<tr><td><br/>"+pageNameMap[num]+':</td><td></td></tr>'
            #print >> sys.stderr,'summarize is '+str(summarize[num].items())
            for item in statNameMap:
                name = item[1]
                key = item[0]
                #print str(key) + ' : ' + str(summarize[num])
                code += '<tr><td align="center">'+ name + "</td><td>" + str(summarize[num][key])+'</td></tr>'
        code += '</table>'
        return code


    def getQuery(self, date):
        res = getquerylist(date)
        return [x.get('key_name') for x in res]

if __name__ == '__main__':
  v = PosterMonitorHanlder()
  v.get()


 



