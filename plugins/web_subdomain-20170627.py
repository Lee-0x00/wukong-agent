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
import requests
req = requests.Session()

#target,result=[]
class WuKong(object):
    def __init__(self,  target = ""):
        self.target = target
        self.url = 'http://api.chaxun.la/toolsAPI/getDomain/'
        self.verify = ""
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Chaxun subdomain api",
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
            timestemp = time.time()
            url = "{0}?0.{1}&callback=&k={2}&page=1&order=default&sort=desc&action=moreson&_={3}&verify={4}".format(
                self.url, timestemp, target , timestemp, self.verify)
            result = json.loads(req.get(url).content)
            if result.get('status') == '1':
                for item in result.get('data'):
                    if is_domain(item.get('domain')):
                        self.result["bug_detail"].append(item.get('domain').encode('gbk'))
            elif result.get('status') == 3:
                pass
            return list(set(self.result))
        except Exception as e:
            return 0

    def download(self, url):
        try:
            r = req.get(url)
            with open("captcha.gif", "wb") as image:     
                image.write(r.content)
            return True
        except Exception, e:
            return False

    def verify_code(self):
        timestemp = time.time()
        imgurl = 'http://api.chaxun.la/api/seccode/?0.{0}'.format(timestemp)
        if self.download(imgurl):
            captcha = Captcha()
            code_result = captcha.verification(filename='captcha.gif')
            self.verify = code_result.get('Result')

# netcraft = WuKong(target ='www.aliyun.com')
# netcraft.run()
# print netcraft.result
