# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: Description 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-01-14 21:04:00

import sys
sys.path.append("..")

from common.captcha import Captcha
from common.wukong_Func import *
from common.wukong_TypeCheck import *
import re,os

class WuKong(object):
	def __init__(self,  target = ""):
		self.target = target
		self.result = {
		"bug_author" : "Bing",
		"bug_name" : "Dns zone transfer",
		"bug_summary" : "黑客可以快速的判定出某个特定zone的所有主机，收集域信息，选择攻击目标，找出未使用的IP地址，黑客可以绕过基于网络的访问控制。", 
		"bug_level" : "Medium" , 
		"bug_detail" : [] ,
		"bug_repair" : "区域传送是DNS常用的功能，区域传送的漏洞也不是没有办法解决的，严格限制允许区域传送的主机即可，例如一个主DNS服务器应该只允许它的从DNS服务器执行区域传送的功能。"
		}

	def run(self):
		if is_domain(self.target) == False :
			return 0
		try:
			test = self.target.split(".")[1:]
			domain  = '.'.join(test)
			cmd_res = os.popen('nslookup -type=ns ' + domain).read()  # fetch DNS Server List
			dns_servers = re.findall('nameserver = ([\w\.]+)', cmd_res)
			if len(dns_servers) == 0:
				pass
			for singledns in dns_servers:
				cmd_res = os.popen('dig @%s axfr %s' % (singledns, domain)).read()
				print cmd_res
				if cmd_res.find('Transfer failed.') < 0 and cmd_res.find('connection timed out') < 0 and cmd_res.find('XFR size') > 0  :
					print '%s %s\n' % (singledns.ljust(30), domain)
					self.result["bug_detail"].append('%s %s\n' % (singledns.ljust(30), domain))
				else:
					pass
		except:
			pass


# netcraft = WuKong(target ='www.lut.edu.cn')
# netcraft.run()
#print netcraft.result 
