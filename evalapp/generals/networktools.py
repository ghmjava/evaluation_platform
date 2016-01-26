#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
print sys.executable
import urllib, urllib2
import simplejson as sj
import pprint
import multiprocessing
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import random
import time

def reqPOST(requrl, post_data, header):
    # send POST request, return json result
    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(requrl, post_data)
    for k,v in header.items():
        req.add_header(k, v)
    res = urllib2.urlopen(req).read()
    res = sj.loads(res)
    #print res
    return res
