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
        self.result = []
        self.captcha = Captcha()
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Sitedossier subdomain api",
        "bug_summary" : "Subdomain search", 
        "bug_level" : "Normal" , 
        "bug_detail" : [] ,
        "bug_repair" : "none"
        }

    def run(self):
        if is_domain(self.target) == False :
            return []
        target = '.'.join(self.target.split(".")[1:])
        try:
            url = 'http://www.sitedossier.com/parentdomain/{0}'.format(target )
            r = self.get_content(url)
            self.parser(r)
            return list(set(self.result))
        except Exception, e:
            return 0

    def get_content(self, url):
        r = http_request_get(url).text
        if self.human_act(r) is True:
            return r
        else:
            self.get_content(url)
            
    def parser(self, response):
        npage = re.search('<a href="/parentdomain/(.*?)"><b>Show', response)
        if npage:
            for sub in self.get_subdomain(response):
                self.result["bug_detail"].append(sub)
            nurl = 'http://www.sitedossier.com/parentdomain/{0}'.format(npage.group(1))
            response = self.get_content(nurl)
            self.parser(response)
        else:
            for sub in self.get_subdomain(response):
                self.result["bug_detail"].append(sub.encode('gbk'))

    def get_subdomain(self, response):
        domain = re.compile(r'(?<=<a href\=\"/site/).*?(?=\">)')
        for sub in domain.findall(response):
            yield sub

    def human_act(self, response):
        if 'auditimage' in response or 'blacklisted' in response:
            imgurl = self.get_audit_img(response)
            if imgurl is not None:
                ret = self.captcha.verification(imgurl)
                if ret.has_key('Result'):
                    self.audit(ret['Result'])
                    return True
                else:
                    raise Exception("captcha_verification_is_empty")
            else:
                raise Exception("audit_img_is_empty")
        else:
            return True

    def audit(self, code):
        payload = {'w':code}
        url = 'http://www.sitedossier.com/audit'
        r = http_request_post(url, payload=payload)

    def get_audit_img(self, response):
        auditimg = re.compile(r'(?<=<img src\=\"/auditimage/).*?(?=\?" alt="Please)')
        imgurl = auditimg.findall(response)[0:]
        if len(imgurl) >= 1:
            imgurl = 'http://www.sitedossier.com/auditimage/{0}'.format(imgurl[0])
            return imgurl
        else:
            return None

    def __str__(self):
        handler = lambda e: str(e)
        return json.dumps(self, indent=2, default=handler)

# netcraft = WuKong(target ='www.aliyun.com')
# netcraft.run()
# print netcraft.result
