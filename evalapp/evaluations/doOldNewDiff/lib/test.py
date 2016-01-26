#coding:utf-8
#!usr/bin/python
from OnlineOfflineDiff import OnlineOfflineDiff

if __name__=="__main__":
	online_url="http://search.virus.meilishuo.com/goodslist/get_goods_list"
	offline_url="http://search.virus.meilishuo.com/goodslist/get_goods_list"
	compare_param="show_num	0.05&tids	0.1"
	obj=OnlineOfflineDiff(online_url,offline_url,{"offset":0,"limit":960,"query":'[" "]',"platform":"web", "sort":'boom', "debug":0, "close_cache":1, }, {'Meilishuo':'uid:9;ip:111.206.87.114;v:1;master:0'},"../data/100.txt", compare_param,"../result/result.txt", 0)
	obj.start()
