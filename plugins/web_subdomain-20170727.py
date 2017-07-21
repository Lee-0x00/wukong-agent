#!/user/bin python
# -*- coding:utf-8 -*- 
# Author:Bing
# Contact:amazing_bing@outlook.com
# DateTime: 2016-12-21 11:46:49
# Description:  coding 

import sys
sys.path.append("..")

from common.captcha import Captcha
from common.wukong_Func import *
from common.wukong_TypeCheck import *

class WuKong(object):
    def __init__(self,  target = "" ):
        self.target = target
        self.url = 'http://i.links.cn/subdomain/'
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Links subdomain api",
        "bug_summary" : "Subdomain search", 
        "bug_level" : "Normal" , 
        "bug_detail" : [] ,
        "bug_repair" : "none"
        }

    def run(self):
        if is_domain(self.target) == False :
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
                if is_domain(item):
                    self.result["bug_detail"].append(item.encode('gbk'))

            return list(set(self.result))
        except Exception as e:
            return 0

# netcraft = WuKong(target ='www.baifubao.com')
# netcraft.run()
# print netcraft.result

