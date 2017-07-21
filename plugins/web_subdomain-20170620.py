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
    def __init__(self,  target = ""):
        self.target = target
        self.website = "https://www.threatminer.org"
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Threatminer subdomain api",
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
            url = "{0}/getData.php?e=subdomains_container&q={1}&t=0&rt=10&p=1".format(self.website, target )
            content = http_request_get(url).content

            _regex = re.compile(r'(?<=<a href\="domain.php\?q=).*?(?=">)')
            for sub in _regex.findall(content):
                if is_domain(sub):
                    self.result["bug_detail"].append(sub)

            return list(set(self.result))
        except Exception as e:
            return 0
            
# netcraft = WuKong(target ='www.lagou.com')
# netcraft.run()
# print netcraft.result
