#!/user/bin python
# -*- coding:utf-8 -*- 
# Author:Bing
# Contact:amazing_bing@outlook.com
# DateTime: 2016-12-21 11:46:49
# Description:  coding 

import sys
sys.path.append("..")

from common.captcha import Captcha
from common.func import *
from common.check import *

import json,re,subprocess,time


class WuKong(object):
    def __init__(self,  target = "", args = ""):
        self.target = target
        self.cookies = args["cookies"]
        
        self.url = 'http://i.links.cn/subdomain/'
        self.result = {
            "bug_author" : "Bing",
            "bug_name" : "Links subdomain api",
            "bug_summary" : "Subdomain search", 
            "bug_level" : "Normal" , 
            "bug_detail" : [] ,
            "bug_repair" : "none"
        }

    def exploit(self):
        if is_Domain(self.target) == False :
            return []
        target = str(".".join(self.target.split(".")[1:]))
        try:
            payload = {
                'b2': 1,
                'b3': 1,
                'b4': 1,
                'domain': target 
            }
            r = http_request_post(self.url,payload=payload).text
            subs = re.compile(r'(?<=value\=\"http://).*?(?=\"><input)')
            for item in subs.findall(r):
                if is_Domain(item):
                    self.result["bug_detail"].append(item.encode('gbk'))

            return list(set(self.result))
        except Exception as e:
            return 0

# netcraft = WuKong(target ='www.aliyun.com',args = {"cookies":"" , "user_pass": "" , "args" : "www" })
# netcraft.exploit()
# print netcraft.result 


