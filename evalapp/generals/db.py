#!/usr/bin/env python

#coding:utf-8

import mysql.connector as mc
import hashlib
import simplejson as sj
import urllib,urllib2
import os,sys
import time, datetime
import traceback
import re
from django.db import connection

def is_connection_usable():
    try:
        connection.connection.ping()
    except:
        return False
    else:
        return True

def takeDataFromMySQL(sql, database='focus', host='172.16.7.139', port=3307, user='mlsreader', password='RMlSxs&^c6OpIAQ1'):
    con = mc.connect(user=user, password=password, host=host, port=port, database=database)
    cur = con.cursor(dictionary=True)
    try:
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        con.close()
        return res
    except:
        #traceback.print_exc()
        cur.close()
        con.close()

def buildDBInfo(MYSQLINI='/home/work/conf/real/bj/mysql/bi/bi.mysql.ini'):
    dbinfo = {}
    with open(MYSQLINI) as f:
        for line in f:
            res = re.search("db=(.*?)\s+host=(\d+\.\d+\.\d+\.\d+)\s+port=(\d{4})\s+weight=(\d)\s+user=(.*?)\s+pass=(.*?)\s+master=(\d)", line.strip('\n'))
            if res == None:
                print line 
                continue
            if len(res.groups()) == 7:
                if res.group(7) == '0':
                    dbinfo[res.group(1)] = {'database':res.group(1), 'host':res.group(2), 'port':int(res.group(3)), 'weight':res.group(4), 'user':res.group(5), 'password':res.group(6), 'master':res.group(7)}
    return dbinfo

DBINFOfromBI = buildDBInfo()
DBINFOfromBRD = buildDBInfo('/home/work/conf/real/bj/mysql/seo/brd.mysql.ini')

def query(dbname, sql, dbinfo=DBINFOfromBI):
    print dbinfo[dbname]
    res = takeDataFromMySQL(sql, database=dbname, host=dbinfo[dbname]['host'], port=dbinfo[dbname]['port'], user=dbinfo[dbname]['user'], password=dbinfo[dbname]['password'])
    return res
    
def getquerylist(dt, platform=2, dblimit=100, dbpos=0, type=1):
    platform_map = {'web':'1', 'mob':'2'}
    last_week = (dt - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    date = dt.strftime('%Y-%m-%d')
    plat = platform_map[platform] if platform in platform_map else 2
    if type == 1:
        sql = "select key_name, pid, sum(pv) as pv from t_brd_query_words_data where date>= '" + last_week \
                + "' and date<='" + date \
                + "' and platform = " + str(plat) \
                + " and word_num = 1 and pid > 0 and key_name != '' group by key_name order by pv desc limit " + str(dbpos) + "," + str(dblimit)
    else:
        sql = "select key_name, pid, sum(pv) as pv from t_brd_query_words_data where date>= '" + last_week \
                + "' and date<='" + date \
                + "' and platform = " + str(plat) \
                + " and  key_name != '' group by key_name order by pv desc limit " + str(dbpos) + "," + str(dblimit)
    results = query('brd_report',sql,DBINFOfromBRD)
    
    return results


if __name__ == "__main__":
    print getquerylist(datetime.date.today())
    

    
