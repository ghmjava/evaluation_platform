#!/usr/bin/env python
#coding:utf-8

import time, datetime
import os, sys
sys.path.append("/home/work/xusiwei/projects/evaluationPlatform/evalapp/")
sys.path.append("/home/work/xusiwei/projects/evaluationPlatform/evalapp/common/")
print sys.path
from generals.db import *

def list_to_dict(rows,key):
    result = {}
    for row in rows:
        result[row[key]] = row
    return result

sql = 'select shop_id, partner_area_id from t_focus_shop_info ;'
areadata = query('focus', sql)
areadict = list_to_dict(areadata,'shop_id')

today=datetime.datetime.now()
weekday = int(today.strftime("%w"))
weekday = 7 if weekday == 0 else weekday
this_week_monday = today - datetime.timedelta(weekday-1) 
sql = 'select shop_id,level from t_focus_shop_level_final where dt = "%s";' % this_week_monday.strftime("%Y-%m-%d")
leveldata = query('focus', sql)
leveldict = list_to_dict(leveldata,'shop_id')

sql = 'select shop_id,periods_dsr from t_focus_shop_daily_health_stat where periods_dsr is not null;'
dsrdata = query('focus', sql)
dsrdict = list_to_dict(dsrdata,'shop_id')


sql = '''
select t1.*, if(t2.intime_response_rate is null, 0, t2.intime_response_rate) as intime_response_rate,
  if(t3.intime_express_rate is null, 0, intime_express_rate) as intime_express_rate,
  if(t2.first_response_time is null, 0, first_response_time) as first_response_time
from
(
  select shop_id, periods_reason_refund_rate, periods_appeal_rate 
  from t_focus_shop_daily_health_stat 
  where dt = ( 
    select max(dt) 
    from t_focus_shop_daily_health_stat
  ) and periods_reason_refund_rate is not null and periods_appeal_rate is not null
) t1
left join
(
  select shop_id, intime_number/question_number as intime_response_rate, total_effective_time/intime_number as first_response_time
  from t_focus_shop_huahua_daily_stat
  where dt = (
    select max(dt)
    from t_focus_shop_huahua_daily_stat
  )
) t2 on t1.shop_id = t2.shop_id
left join
(
  select shop_id, intime_express_rate
  from t_focus_shop_express_stat
  where dt = (
    select max(dt)
    from t_focus_shop_express_stat 
  )
) t3 on t1.shop_id = t3.shop_id
'''

service_data = query('focus', sql)
service_dict = list_to_dict(service_data, 'shop_id')

sql = 'SELECT twitter_id FROM `campaign_goods_info` WHERE `aid` in (2230,2240,2232,2234) and audit_status in (4)'
active_data = query('brd_shop', sql)
active_dict = list_to_dict(active_data, 'twitter_id')
header=["twitter_id"]
#active_dict={}
#with open("/home/work/tarsier_online/utils/cs_act_tids.txt") as fobj:
#  for line in fobj:
#    parts = line.strip().split("\t")
#    parts = map(int, parts)
#    twitter_id = int(parts[0])
#    content = dict(zip(header, parts))
#    active_dict[twitter_id] = content

sql = 'select * from im_shop_status where shop_status = 1'
shop_service_data = query('im', sql)
shop_service_dict = list_to_dict(shop_service_data, 'shop_id')

sql = "select distinct twitter_id, twitter_sort from campaign_theme_goods where aid in (%s)" % ('111111111111')
dacu_goods = query("brd_shop",sql)

class NormCountTools(object) :

    style_score_dict = {4:4, 3:3, 2:2}
    pic_score_dict = {3:0, 2:-0.5}
    style_score_list = (4,3)
    day_is_new = 7
    shows_is_boom = 20000
    gmv_is_boom = 14000
    round = 2
    offset = 0
    support_shop_ids = []

    def __init__(self, data, end, offset = 0):
        self.tids = map(lambda x:str(x),data['tids'][offset:end]) if data else []
        self.ext = data['ext_info'] if data else {}
        self.total = len(self.tids) * 1.0
        self.offset = offset
        self.support_shop_ids = self.getSupportShops()
        self.bad_shop_ids = self.getBadShops()
        self.dacu_goods = dacu_goods

        self.areadict = areadict

        self.leveldict = leveldict

        self.dsrdict = dsrdict

        self.service_dict = service_dict 

    def getDsr():
        sql = 'select shop_id,periods_dsr from t_focus_shop_daily_health_stat where periods_dsr is not null;'
        dsrdata = query('focus', sql)
        list_to_dict(dsrdata,'shop_id')
      
    def area(self,r):
      #self.aredict
      l = []
      for tid in self.tids:
        if self.ext[tid].has_key('brd_shop_id') and  self.areadict.has_key(self.ext[tid]['brd_shop_id']) and  self.areadict[self.ext[tid]['brd_shop_id']]['partner_area_id'] == r:
          l.append(tid)
      return self.to_rate(l)

    def avg_ctr(self):
      return self.to_score(self.ext[tid]['brd_shop_ctr_predict_refer']  for tid in self.tids if self.ext[tid].has_key('twitter_id'))

    def shop_service(self):
      tmp = []
      for tid in self.tids:
        if self.ext[tid].has_key('twitter_id') and shop_service_dict.has_key(self.ext[tid]['brd_shop_id']):
          tmp.append(tid)
      return self.to_rate(tmp)

    def avg_dsr(self):
      return self.to_score(self.dsrdict[self.ext[tid]['brd_shop_id']]['periods_dsr'] for tid in self.tids  if self.ext[tid].has_key('brd_shop_id') if self.dsrdict.has_key(self.ext[tid]['brd_shop_id']))

    def active_fill_rate(self):
        return self.to_rate([tid for tid in self.tids  if active_dict.has_key(long(tid))])

    def avg_reason_refund_rate(self):
      return self.to_score(self.service_dict[self.ext[tid]['brd_shop_id']]['periods_reason_refund_rate'] for tid in self.tids  if self.ext[tid].has_key('brd_shop_id') if self.service_dict.has_key(self.ext[tid]['brd_shop_id']))

    def avg_appeal_rate(self):
      return self.to_score(self.service_dict[self.ext[tid]['brd_shop_id']]['periods_appeal_rate'] for tid in self.tids  if self.ext[tid].has_key('brd_shop_id') if self.service_dict.has_key(self.ext[tid]['brd_shop_id']))

    def avg_intime_response_rate(self):
      return self.to_score(self.service_dict[self.ext[tid]['brd_shop_id']]['intime_response_rate'] for tid in self.tids  if self.ext[tid].has_key('brd_shop_id') if self.service_dict.has_key(self.ext[tid]['brd_shop_id']))

    def avg_first_response_time(self):
      return self.to_score(self.service_dict[self.ext[tid]['brd_shop_id']]['first_response_time'] for tid in self.tids  if self.ext[tid].has_key('brd_shop_id') if self.service_dict.has_key(self.ext[tid]['brd_shop_id']))


    def avg_express_rate(self):
      return self.to_score(self.service_dict[self.ext[tid]['brd_shop_id']]['intime_express_rate'] for tid in self.tids  if self.ext[tid].has_key('brd_shop_id') if self.service_dict.has_key(self.ext[tid]['brd_shop_id']))



    def golden_fill_rate(self):
      return self.key_rate('is_gold_goods', 1)

    def top_fill_rate(self):
      return self.key_rate('goods_level', 1)

    def shoplevel(self,level):
      l = []
      for tid in self.tids:
        if self.ext[tid].has_key('brd_shop_id') and  self.leveldict.has_key(self.ext[tid]['brd_shop_id']) and  self.leveldict[self.ext[tid]['brd_shop_id']]['level'] == level:
        #if self.ext[tid].has_key('brd_shop_id') and  self.leveldict.has_key(self.ext[tid]['brd_shop_id']) :
          l.append(tid)
      return self.to_rate(l)

    def fashion_score(self):
        f = open('/tmp/yue', 'a+')
        f.write(str(self.tids))
        f.write("\n!!!!!\n")
        f.write(str(self.ext))
        f.close()
        return self.to_score(self.style_score_dict.get(self.ext[tid]['style_score'], 0) + self.pic_score_dict.get(self.ext[tid]['pic_score'], 0) for tid in self.tids if self.ext[tid].has_key('twitter_id'))

    def fashion_rate(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id') if self.ext[tid]['style_score'] in self.style_score_list])

    def new_score(self):
        return self.to_score((time.time() - self.ext[tid]['twitter_create_time'])/86400 for tid in self.tids  if self.ext[tid].has_key('twitter_id'))

    def new_rate(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id') if (time.time() - self.ext[tid]['twitter_create_time']) < self.day_is_new*86400])
        #return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id') if self.ext[tid]['brd_shop_shows_poster'] < 40000])

    def boom_score(self):
        return self.to_score(self.ext[tid]['brd_shop_score_poster'] for tid in self.tids if self.ext[tid].has_key('twitter_id'))


    def boom_rate(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id')  if self.ext[tid]['brd_shop_score_poster'] >= 1.5 ])

    def ecpmscore(self):
        #self.ext[tid]['brd_shop_gmv_poster'] for tid in self.tids
        #print 'this is ecpm',float(self.ext[tid]['brd_shop_gmv_poster'])/self.ext[tid]['brd_shop_shows_poster'] for tid in self.tids if self.ext[tid].has_key('twitter_id') if self.ext[tid]['brd_shop_shows_poster'] >= 1000 if time.time() - self.ext[tid]['twitter_create_time'] > 10*86400
        list = []
        for tid in self.tids:
            if self.ext[tid].has_key('twitter_id') and self.ext[tid]['brd_shop_shows_poster'] >= 1000 and time.time() - self.ext[tid]['twitter_create_time'] > 10*86400:
                list.append(float(self.ext[tid]['brd_shop_gmv_poster'])/self.ext[tid]['brd_shop_shows_poster'])
                #print self.ext[tid]['brd_shop_gmv_poster'],self.ext[tid]['brd_shop_shows_poster']
        if len(list) == 0 :
            return 0
        #print list
        #print round(float(sum(list))*1000 / len(list), self.round)
        return round(float(sum(list))*1000 / len(list), self.round)

        #return self.to_score(list1)
        #return 0.0

    def popular_score(self):
        """这里的点展分需要可靠?"""
        return self.to_score(self.ext[tid]['brd_shop_ctr_predict_refer']  for tid in self.tids if self.ext[tid].has_key('twitter_id'))

    def popular_rate(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id') if self.ext[tid]['brd_shop_shows_poster'] >= 97000])

    def health_degree(self):
        return self.to_score(self.ext[tid]['shop_health_score']  for tid in self.tids if self.ext[tid].has_key('twitter_id'))

    def bad_goods_rate(self):
        return self.to_rate([tid for tid in self.tids if self.ext[tid].has_key('twitter_id') if self.ext[tid]['brd_shop_black_poster'] or self.ext[tid]['brd_shop_id'] in self.bad_shop_ids])

    def chuchuang_rate(self):
        return self.to_rate([tid for tid in self.tids if self.ext[tid].has_key('twitter_id') if 'hot_position_weight' in self.ext[tid] and self.ext[tid]['hot_position_weight'] > 0])

    def high_transform_rate(self):
        return self.to_rate([tid for tid in self.tids if self.ext[tid].has_key('twitter_id') if (1000 * self.ext[tid]['brd_shop_gmv_poster']/(1+self.ext[tid]['brd_shop_shows_poster']))>3])

    def high_transform_score(self):
        return self.to_score(1000 * self.ext[tid]['brd_shop_gmv_poster']/(1+self.ext[tid]['brd_shop_shows_poster']) for tid in self.tids if self.ext[tid].has_key('twitter_id') )

    def price(self):
        return self.to_score(self.ext[tid]['goods_price']  for tid in self.tids if self.ext[tid].has_key('twitter_id'))

    def acg_show(self):
        start = 1600
        offset_rank = 160 - self.offset
        rate = 0.0
        for tid in self.tids:
            if self.ext[tid].has_key('twitter_id'):
                if self.ext[tid]['goods_type'] == 999:
                    rate += offset_rank
            offset_rank -= 1
        return round(rate / 1280000.0, 4)

    def acg_fill(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id') if self.ext[tid]['goods_type'] == 999 ])

    def support_show(self):
        start = 1600
        offset_rank = 160 - self.offset
        rate = 0.0
        for tid in self.tids:
            if self.ext[tid].has_key('twitter_id'):
                if self.ext[tid]['brd_shop_id'] in self.support_shop_ids:
                    rate += offset_rank
            offset_rank -= 1
        return round(rate / 1280000.0, 2)

    def support_fill(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id')  if self.ext[tid]['brd_shop_id'] in self.support_shop_ids])

    def autumn_new(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_id') if self.ext[tid]['autumn_new'] == 1 ])

    def gmv_total(self):
        return sum(1 for tid in self.tids if self.ext[tid].has_key('twitter_id') and self.ext[tid]['gmv_thirty_days'] > 14000)

    def pic_score_rate_3(self):
        return self.key_rate('pic_score', 3)

    def pic_score_rate_2(self):
        return self.key_rate('pic_score', 2)

    def pic_score_rate_1(self):
        return self.key_rate('pic_score', 1)

    def pic_score_rate_4(self):
        return self.key_rate('pic_score', 4)

    def style_score_rate_4(self):
        return self.key_rate('style_score', 4)

    def style_score_rate_3(self):
        return self.key_rate('style_score', 3)

    def style_score_rate_2(self):
        return self.key_rate('style_score', 2)

    def style_score_rate_1(self):
        return self.key_rate('style_score', 1)

    def dacu_goods_rate(self):
        tids = []
        for info in self.dacu_goods:
            tids.append(info['twitter_id'])
        return self.to_rate([tid for tid in self.tids if self.ext[tid].has_key('twitter_id') and self.ext[tid]['twitter_id'] in tids ])

    def ka_rate(self):
        return self.to_rate([tid for tid in self.tids if self.ext[tid].has_key('brd_shop_id') and self.ext[tid]['brd_shop_id'] in [100014, 100556, 100604, 100687, 100843, 101313, 101633, 101645, 101661, 101671, 101713, 101723, 101747, 101791, 101841, 101847, 101851, 101937, 101943, 101949, 102063, 102159, 102225, 102357, 102395, 102441, 102493, 102703, 102729, 102895, 102901, 102973, 102997, 103003, 103027, 103083, 103391, 103417, 103509, 103599, 103601, 103759, 103811, 103879, 104141, 104205, 104223, 104395, 104521, 104543, 104777, 104815, 104875, 105059, 105191, 105329, 105425, 105675, 105699, 105745, 105993, 106365, 106517, 106621, 107083, 107441, 107563, 108101, 108107, 108135, 108159, 108174, 108183, 108442, 111090, 111136, 111220, 111346, 111348, 111744, 111871, 113077, 113486, 114130, 115415, 119399, 120593, 124201, 124705, 126277, 128229, 132373, 133295, 133559, 144029, 145313, 155151]])

    def create_time_new(self):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key('twitter_create_time') and self.ext[tid]['twitter_create_time'] >= 1405785600 ])

    def key_rate(self, key, score):
        return self.to_rate([tid for tid in self.tids  if self.ext[tid].has_key(key) and self.ext[tid][key] == score ])


    def to_score(self, to_sum):
        if self.total == 0:
            return 0
        return round(float(sum(to_sum)) / self.total, self.round)

    def to_rate(self, to_len):
        if not to_len:
            return 0
        if self.total == 0:
            return 0
        return round(len(to_len) / self.total, self.round)


    def getarea(self,data,v):
        area = data[v['shopid']]['partner_area_id']
        if area == 1:
          return '华东'
        if area == 2:
          return '华北'
        if area == 3:
          return '华南'
        return 'default'   

    def getSupportShops(self):
        """
        获取top pv 100 poster ids
        """
        return []
        res = query('focus', "select shop_id from t_focus_shop_info where level = 10")
        return [int(x.get('shop_id')) for x in res]

    def getBadShops(self):
        return []
        res = query('focus', "select shop_id from t_focus_shop_info where level = -10")
        return [int(x.get('shop_id')) for x in res]


