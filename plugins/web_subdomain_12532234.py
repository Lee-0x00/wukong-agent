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

from random import Random,uniform
from urllib import quote

def random_sleep():
    time.sleep(uniform(0,2))

def random_str(randomlength=8):
    rstr = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        rstr += chars[random.randint(0, length)]
    return rstr.lower()

class WuKong(object):
    def __init__(self,  target = "" ):
        self.target = target
        self.token = ""
        self.subjects = []
        self.hashs = []
        self.num_result = 0
        self.website = 'https://www.google.com/transparencyreport/jsonp/ct'
        self.result = {
        "bug_author" : "Bing",
        "bug_name" : "Google subdomain api",
        "bug_summary" : "Subdomain search", 
        "bug_level" : "Normal" , 
        "bug_detail" : [] ,
        "bug_repair" : "none"
        }

    def run(self):
        if is_domain(self.target) == False :
            return []
        target = '.'.join(self.target.split(".")[1:])
        self.parser_subject(target)
        self.hashs = list(set(self.hashs)) # unique sort hash
        self.parser_dnsname()
        self.result["bug_detail"] = list(set(self.result["bug_detail"]))
        #self.subjects = list(set(self.subjects))
        return 0

    def parser_subject(self,target):
        try:
            callback = random_str()
            url = '{0}/search?domain={1}&incl_exp=true&incl_sub=true&token={2}&c={3}'.format(
                    self.website, target , quote(self.token), callback)
            content = http_request_get(url).content
            result = json.loads(content[27:-3])
            self.token = result.get('nextPageToken')
            for subject in result.get('results'):
                if subject.get('subject'):
                    self.result["bug_detail"].append(subject.get('subject').encode("gbk"))
                if subject.get('hash'):
                    self.hashs.append(subject.get('hash').encode("gbk"))
        except Exception as e:
            pass

        if self.token:
            self.parser_subject()

    def parser_dnsname(self):
        for hashstr in self.hashs:
            try:
                callback = random_str()
                url = '{0}/cert?hash={1}&c={2}'.format(
                        self.website, quote(hashstr), callback)
                content = http_request_get(url).content
                result = json.loads(content[27:-3])
                if result.get('result').get('subject'):
                    self.subjects.append(result.get('result').get('subject').encode("gbk"))
                if result.get('result').get('dnsNames'):
                    self.result["bug_detail"].extend(result.get('result').get('dnsNames').encode("gbk"))
            except Exception as e:
                pass
            random_sleep()

# netcraft = WuKong(target='www.lagou.com')
# netcraft.run()
# print netcraft.result
