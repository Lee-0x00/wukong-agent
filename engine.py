# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import imp, os, time, random, re
from core.settings import PLUGIN_PATH			#插件路径
from utils.api import *							#自定义上传日志


class wkengine(object):
	'''
	扫描主引擎
	'''

	def custom_get_poc_path(self, scan_type = [""], no_scan = []): 
		'''
		自定义获取poc完整路径 --finish
		print(custom_get_poc_path([""],["123"]))
		'''
		result = []
		plugin_files = os.listdir(PLUGIN_PATH)

		#需要扫描的模块
		poc_regex = []
		for line in scan_type :
			poc_regex.append( re.compile('^(wk-).*?' + line + '.*?\.py$') )

		for poc_file in plugin_files:
			for regex in poc_regex :
				match = regex.search(poc_file) 
				if match :
					result.append( ( len(match.group()), match.start(), os.path.join(PLUGIN_PATH, poc_file) ) )

		#不需要扫描的模块
		no_poc_regex = []
		for line in no_scan :
			no_poc_regex.append( re.compile('^(wk-).*?' + line + '.*?\.py$') )

		for poc_file in plugin_files:
			for regex in no_poc_regex :
				match = regex.search(poc_file) 
				if match :
					try:
						result.remove( ( len(match.group()), match.start(), os.path.join(PLUGIN_PATH, poc_file) ) )
					except:
						pass
		return [x for _, _, x in sorted(result)]


	def launcher(self, poc_file, target) :
		'''
		执行任务
		'''
		start = time.time()

		taskid = target["taskid"]
		host = target["host"]
		poc_filename = poc_file.split("exploit",1)[1]
		custom_upload_log(taskid, 1, "%s ; running ... " % str(poc_filename) )

		try:
			poc_class = imp.load_source('Exploit', poc_file )
			data = poc_class.Exploit(args = target)
			data.exploit()
			result = data.result
			status = result["status"]

			if status:
				for line in result["data"] :
					result = line["bug_result"]
					if len(result) > 0 :
						custom_upload_result(taskid, host, line)

				end = time.time()
				custom_upload_log(taskid, 20, str(poc_filename) + "; time: " + "%0.2f seconds; " % (end - start) + str("finish") )
			else:
				end = time.time()
				custom_upload_log(taskid, 20, str(poc_filename) + "; time: " + "%0.2f seconds;" % (end - start) + str("finish; but no result") )
		except Exception as e:
			message = e.__str__()
			end = time.time()
			custom_upload_log(taskid, 20, str(poc_filename) + "; time: " + "%0.2f seconds; error: " % (end - start) + str(message) )

		return True


	def single(self, target, plugins = []):
		'''
		插件式扫描程序主入口
		---------------
		'''
		taskid = target["taskid"]
		host = target["host"]

		#start scan
		start_text = {'bug_name': 'start', 'bug_author': '', 'bug_level': '', 'bug_type': '', 'bug_ref': '', 'bug_desc': '', 'bug_result': [], 'bug_repair': ''}
		custom_upload_result(taskid, host, start_text)

		#poc scan start 
		custom_upload_log(taskid, 1, "poc task start ...")
		poc_list = self.custom_get_poc_path(plugins,[])
		for func in poc_list :
			self.launcher(func, target)
		
		#finish task & make pdf
		finish_text = {'bug_name': 'finish', 'bug_author': '', 'bug_level': '', 'bug_type': '', 'bug_ref': '', 'bug_desc': '', 'bug_result': [], 'bug_repair': ''}
		custom_upload_result(taskid, host, finish_text)
		make_pdf_report(host, taskid)
		custom_upload_log(taskid, 1, "All finish ...")
		f_result = open("result.txt", 'a+')
		f_result.write("%s;%s;finish" % (taskid,host) )
		f_result.write("\r\n")
		f_result.close()

	def default(self, target):
		'''
		全部扫描程序主入口
		---------------
		'''
		taskid = target["taskid"]
		host = target["host"]

		#program starting
		start_text = {'bug_name': 'start', 'bug_author': '', 'bug_level': '', 'bug_type': '', 'bug_ref': '', 'bug_desc': '', 'bug_result': [], 'bug_repair': ''}
		custom_upload_result(taskid, host, start_text)
		
		#port scan start 
		custom_upload_log(taskid, 1, "port scan start ...")
		poc_list = self.custom_get_poc_path(["123"],[])
		for func in poc_list :
			self.launcher(func, target)

		#awvs scan start 
		custom_upload_log(taskid, 1, "awvs scan start ...")
		poc_list = self.custom_get_poc_path(["awvs","234"],[])

		for func in poc_list :
			self.launcher(func, target)


		#finish task & make pdf
		finish_text = {'bug_name': 'finish', 'bug_author': '', 'bug_level': '', 'bug_type': '', 'bug_ref': '', 'bug_desc': '', 'bug_result': [], 'bug_repair': ''}
		custom_upload_result(taskid, host, finish_text)
		make_pdf_report(host, taskid)
		custom_upload_log(taskid, 1, "All finish ...")
		f_result = open("result.txt", 'a+')
		f_result.write("%s;%s;finish" % (taskid,host) )
		f_result.write("\r\n")
		f_result.close()
