# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: Description 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-01-14 17:05:46

import sys
sys.path.append("..")

from common.captcha import Captcha
from common.wukong_Func import *
from common.wukong_TypeCheck import *
import requests,socket

class WuKong(object):
	def __init__(self,  target = "",args = ""):
		self.target = target
		self.args = args
		self.port = 6379
		self.result = {
			"bug_author" : "bing",
			"bug_name" : "redis 爆破",
			"bug_summary" : "redis port brute", 
			"bug_level" : "high" , 
			"bug_detail" : [] ,
			"bug_repair" : "disable vulnerability password"
			}


	def run(self):
		if is_domain(self.target) or is_host(self.target) :
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				#s.settimeout(0.1)
				s.connect((self.target,int(self.port)))
				s.send("INFO\r\n")
				result = s.recv(1024)
				if "redis_version" in result:
				 	self.result["bug_detail"].append("unauthorized")
				else:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((self.target,int(self.port)))
					s.send("AUTH %s\r\n"%(self.args))
					result = s.recv(1024)
					if '+OK' in result:
						self.result["bug_detail"].append(self.args)
			except Exception,e:
				pass


# t = BingScan(target="127.0.0.1",args = "1234" )
# t.run()
# print t.result
