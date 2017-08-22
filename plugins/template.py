# -*- coding: UTF-8 -*- 
# __author__ : Bing
# email : amazing_bing@outlook.com
# date : 2017��8��7��

from common.captcha import Captcha
from common.func import *
from common.check import *


class WuKong(object):
    def __init__(self,  target = "", args = ""):    #result对应键的值可更改，其他都必须继承
        self.target = target
        self.args = args["args"]
        self.cookies = args["cookies"]
        self.user_pass = args["user_pass"]
        self.result = {
            "bug_author" : "Bing",
            "bug_name" : "Netcraft subdomain api",
            "bug_summary" : "Subdomain search", 
            "bug_level" : "Normal" , 
            "bug_detail" : [] ,
            "bug_repair" : "none"
        }        
        
    def verify(self):
        pass#可写也可不写
    
    def exploit(self):
        pass#必写函数