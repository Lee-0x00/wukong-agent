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
import dns.resolver


class WuKong(object):
	def __init__(self,  target = "", args = ""):
		self.target = target
		self.args = args
		self.result = {
			"bug_author" : "bing",
			"bug_name" : "brute subdomain script",
			"bug_summary" : "subdomain brute", 
			"bug_level" : "normal" , 
			"bug_detail" : [] ,
			"bug_repair" : "none"
			}

	def domain(self,test):
		try:
			dns_server = ["114.114.114.114","114.114.115.115","180.76.76.76","223.5.5.5","223.6.6.6","8.8.8.8"]
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = ["114.114.114.114","114.114.115.115","180.76.76.76","223.5.5.5","223.6.6.6","8.8.8.8"]
			target = str(test)
			answers = my_resolver.query(target)
			ips = ', '.join([answer.address for answer in answers])
			return (ips,target)
		except:
			return ''

	def run(self):
		if is_domain(self.target) == False :
			return []
		try:
			target = str(self.args)+'.'+ str(".".join(self.target.split(".")[1:]))
			result = self.domain(target)
			if result == "":
				pass
			else:
				self.result["bug_detail"].append(target)
		except:
			pass


# netcraft = WuKong(target ='www.aliyun.com',args = 'www')
# netcraft.run()
# print netcraft.result 
