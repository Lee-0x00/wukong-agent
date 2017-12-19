# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

import requests, json, re, time
from utils.exploit import *

class wk(object):
	def __init__(self, target):
		self.server_host = "127.0.0.1"
		self.server_port = "8775"
		self.headers = {'Content-Type': 'application/json'}
		self.info = {
			# 输入参数
			"protorl" : target["scan_protorl"],
			"host" : target["scan_target"],    
			"port" : target["scan_port"],
			"cookie" : target["scan_cookie"],
			"proxy" : target["scan_proxy"],
			"user_agent" : random_useragent(target["scan_user_agent"]),
			"fuzzing" : target["fuzzing"]
		}
		self.result = [{
			# 结果信息
			"status" : False,
			"data" : {
				"bug_name" : "sql injection",
				"bug_author" : "Bing",
				"bug_level" : high,
				"bug_type" : injection,
				"bug_ref" : "",
				"bug_desc" : "",
				"bug_result" : "",
				"bug_repair" : ""
			},
		}]


	def connect(self, method, resource, data = None):
		if method == "POST":
			try:
				r = requests.post(url = str("http://" + self.server_host + ":" + self.server_port) + "/" + str(resource) , data = data, headers = self.headers, verify= False)
			except:
				return False
		elif method == "GET":
			try:
				r = requests.get(url = str("http://" + self.server_host + ":" + self.server_port) + "/" + str(resource) , headers = self.headers, verify= False)
			except:
				return False

		if r.status_code == 200:
			try:
				data = r.json()
			except:
				data = r.content
			return data       
		else:
			return False


	def create_task(self):
		#新建扫描任务
		result = self.connect(method = "GET", resource = "task/new")
		return result


	def del_task(self, taskid):	
		#删除任务
		result = self.connect(method = "GET", resource = "task/" + str(taskid) + "/delete")
		return result


	def set_args(self, taskid, method = '', url = '', cookie = '', referer = '', data = '', level = 1):
		#设置扫描参数
		scan_options = {
			'cookie' : "{}".format(cookie),
			'data' : "{}".format(data),
			'url' : "{}".format(url),
			'method' : "{}".format(method),
			'level' : level,
			'randomAgent': True, 
			'referer': referer, 
			'host': "", 
		}
		result = self.connect(method = "POST", resource = "option/{0}/set".format(taskid), data = json.dumps(scan_options))
		return result


	def start_task(self, taskid, url):
		#开始任务 scan/{}/start
		scan_options = {}
		scan_options['url'] = url
		result = self.connect(method = "POST", resource = "scan/{0}/start".format(taskid), data=json.dumps(scan_options))
		return result


	def status_task(self, taskid):	
		#查看任务 scan/<taskid>/status
		result = self.connect(method = "GET", resource = "scan/{0}/status".format(taskid) )
		return result


	def	get_data(self,taskid):
		#查看结果
		result = self.connect(method="GET", resource = "scan/{0}/data".format(taskid))
		return result


	def exploit(self):
		scan_options = self.info["fuzzing"]["brute_char"]
		method = scan_options["method"]
		url = scan_options["url"]
		cookie = self.info["cookie"]
		referer = scan_options["referer"]
		data = scan_options["data"]

		#新建任务
		taskid = self.create_task()["taskid"]
		#设置参数
		result = self.set_args(taskid = taskid, method = method, url = url, cookie = cookie, referer = referer, data = data, level = 3)['success']
		if result:
			#任务开始
			start_status = self.start_task(taskid = taskid, url = url)['success']
			if start_status :
				while True :
					#任务状态
					task_status = self.status_task(taskid = taskid)['status']
					if task_status == 'terminated' :
						#任务日志
						data_result = self.get_data(taskid = taskid)
						inject_result = data_result['success']
						inject_data = data_result["data"]
						if inject_result and len(inject_data) > 0:
							#存在注入,保存结果
							inject_title = data_result['data'][0]["value"][0]["data"]
							#print(inject_title)
							result = {}
							result["status"] = True
							result["data"] = {}
							result["data"]["bug_name"] = "sql injection"
							result["data"]["bug_author"] = "Bing"
							result["data"]["bug_level"] = high
							result["data"]["bug_type"] = injection
							result["data"]["bug_ref"] = ""
							result["data"]["bug_desc"] = ""
							result["data"]["bug_result"] = inject_title
							result["data"]["bug_repair"] = "对用户输入数据做验证，sql语句预编译处理!"
							self.result.append(result)
							#删除任务
							self.del_task(taskid)
							break
						else:
							#无注入
							break
					time.sleep(3)
				return True
			else:
				return True
		else:
			return True


# info = {
#     'scan_taskid': '3', 
#     'scan_protorl': 'http://', 
#     'scan_target': 'localhost', 
#     'scan_port': '5000', 
#     'scan_cookie': 'sdf', 
#     'scan_proxy': 'sdf', 
#     'scan_user_agent': True, 
#     'plugin_name': 'sqlmap', 
#     'plugin_file': 'plugins/wk-sqlmap-00.py', 
#     'model': 'brute', 
#     'fuzzing': {'user_pwd': '', 'brute_char': {"method":"POST", "url":"http://localhost:5000/test", "referer":"", "data":"name=tes"}
#     }
# }
# t = wk(info)
# t.exploit()
# print(t.result)
