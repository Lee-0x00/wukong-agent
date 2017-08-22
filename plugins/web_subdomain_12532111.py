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

import json

class WuKong(object):
    def __init__(self,  target = "", args = ""):
        self.target = target
        self.cookies = args["cookies"]
        
        self.website = "https://www.threatcrowd.org"
        self.result = {
            "bug_author" : "Bing",
            "bug_name" : "Netcraft subdomain api",
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
            url = "{0}/searchApi/v2/domain/report/?domain={1}".format(self.website, target )
            content = http_request_get(url).content

            for sub in json.loads(content).get('subdomains'):
                if is_Domain(sub):
                    self.result["bug_detail"].append(sub.encode('gbk'))

            return list(set(self.result))
        except:
            pass

# netcraft = WuKong(target ='www.aliyun.com',args = {"cookies":"" , "user_pass": "" , "args" : "www" })
# netcraft.exploit()
# print netcraft.result 
