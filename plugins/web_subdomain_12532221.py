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
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Netcraft subdomain api",
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
            self.fetch_chinaz(target)
            self.fetch_alexa_cn(target)
            return list(set(self.result))
        except Exception as e:
            return 0

    def fetch_chinaz(self,target):
        url = 'http://alexa.chinaz.com/?domain={0}'.format(target )
        r = http_request_get(url).content
        subs = re.compile(r'(?<="\>\r\n<li>).*?(?=</li>)')
        result = subs.findall(r)
        for sub in result:
            if is_domain(sub):
                self.result["bug_detail"].append(sub)

    def fetch_alexa_cn(self,target):
        sign = self.get_sign_alexa_cn(target)
        if sign is None:
            raise Exception("sign_fetch_is_failed")
        else:
            (domain,sig,keyt) = sign

        pre_domain = target .split('.')[0]

        url = 'http://www.alexa.cn/api_150710.php'
        payload = {
            'url': domain,
            'sig': sig,
            'keyt': keyt,
            }
        r = http_request_post(url, payload=payload).text

        for sub in r.split('*')[-1:][0].split('__'):
            if sub.split(':')[0:1][0] == 'OTHER':
                break
            else:
                sub_name = sub.split(':')[0:1][0]
                sub_name = ''.join((sub_name.split(pre_domain)[0], domain))
                if is_domain(sub_name):
                    self.result.append(sub_name)

    def get_sign_alexa_cn(self,target):
        url = 'http://www.alexa.cn/index.php?url={0}'.format(target )
        r = http_request_get(url).text
        sign = re.compile(r'(?<=showHint\(\').*?(?=\'\);)').findall(r)
        if len(sign) >= 1:
            return sign[0].split(',')
        else:
            return None

# netcraft = WuKong(target ='www.lagou.com')
# netcraft.run()
# print netcraft.result
