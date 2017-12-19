# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39

import gevent, time, os, imp, socket, psutil         
from multiprocessing import Process
from gevent import monkey; monkey.patch_all()
from utils.func import *


def launcher(poc_file, target):
	taskid = target["scan_taskid"]
	host = target["scan_target"]
	model = target["model"]
	plugin_name = target["plugin_name"]
	plugin_file = target["plugin_file"]

	program_log({
		"taskid" : taskid, 
		"model" : model, 
		"plugin_name" : plugin_name, 
		"status" : 1, 
		"info" : "poc running"
	})

	try:
		poc_class = imp.load_source('wk', poc_file )
		t = poc_class.wk(target = target)
		t.exploit()
		result = t.result
		program_result(taskid, host, model, plugin_name, result)

		program_log({
			"taskid" : taskid, 
			"model" : model, 
			"plugin_name" : plugin_name, 
			"status" : 2, 
			"info" : "poc finishing"
		})
	except Exception as e:
		message = e.__str__()
		program_log({
			"taskid" : taskid, 
			"model" : model, 
			"plugin_name" : plugin_name, 
			"status" : 3, 
			"info" : message
		})


def custom_scan(scan_model, num = 5):
	while True:	
		scan_que = get_task("{0}".format(scan_model), num)
		if len(scan_que) > 0 :
			jobs = []
			for target in scan_que:
				taskid = target["scan_taskid"]
				model = target["model"]
				plugin_name = target["plugin_name"]
				plugins = target["plugin_file"].split('-')[1]

				poc_file = get_poc_path(plugins)
				if poc_file :
					jobs.append(gevent.spawn(launcher, poc_file, target))
				else:
					program_log({
						"taskid" : taskid, 
						"model" : model, 
						"plugin_name" : plugin_name, 
						"status" : 3, 
						"info" : "no poc"
					})
			gevent.joinall(jobs)

		else:
			system_log({ "status" : 1, "model" : "{0}".format(scan_model), "info" : "waitting task"})
			time.sleep(5)


if __name__ == '__main__':
	print( 'Run task %s (%s)...' % ("wk scanner engine", os.getpid()) )
	start = time.time()
	#开启多个服务模块
	func_list = [("third", 200,), ("brute", 200,), ("poc", 200,)]
	work = []
	for poc_args in func_list :
		p = Process(target = custom_scan, args=poc_args )
		p.start()
		work.append(p)   		

	for job in work:
		job.join()

	end = time.time()
	print( 'Task %s runs %0.2f seconds.' % ("wk scanner engine", (end - start)) )





