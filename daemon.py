# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

from core.settings import *
from engine import wkengine 					#主引擎
from utils.api import custom_divide_domain		#工具
from multiprocessing import Pool 				#多进程任务
from multiprocessing import Process
import time, os, random, redis


def custom_scan(target) :
	'''
	执行扫描任务
	'''
	scan_taskid = target["taskid"]
	scan_host = target["host"]
	scan_cookies = target["cookie"]
	try:
	    plugins = target["plugins"].split(",")
	except:
	    plugins = ["all"]
	scan_plugins = plugins
	host_protocol , host_name , host_port = custom_divide_domain(scan_host)

	scan_task =	{
			"taskid" : scan_taskid,
			"protorl" : host_protocol,
			"host" : host_name, 
			"port" : host_port,
			"cookie" : scan_cookies,
		}	

	print( 'Run task %s (%s)...' % (scan_taskid, os.getpid()) )
	#任务开始
	start = time.time()   
	print("扫描的插件个数： %d " % len(plugins), plugins )   
	if "all" in plugins :
		wkengine().default(scan_task)
	else:
		wkengine().single(scan_task, scan_plugins)

	#任务完成
	end = time.time()
	print( 'Task %s runs %0.2f seconds.' % (scan_taskid, (end - start)) )
	return scan_taskid


def custom_process(target_list) :
	'''
	自定义多进程扫描任务
	'''
	print('Run %s (%s)...' % ("wkengine", os.getpid()) )
	start = time.time()

	p = Pool(4)
	for target in target_list :
		p.apply_async(custom_scan, args=(target,))

	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	print('All subprocesses done.')


if __name__=='__main__':
	'''
	循环获取任务队列
	'''     
	usage = """
	_          __  _   _   _   _    _____   __   _   _____  
	| |        / / | | | | | | / /  /  _  \ |  \ | | /  ___| 
	| |  __   / /  | | | | | |/ /   | | | | |   \| | | |     
	| | /  | / /   | | | | | |\ \   | | | | | |\   | | |  _  
	| |/   |/ /    | |_| | | | \ \  | |_| | | | \  | | |_| | 
	|___/|___/     \_____/ |_|  \_\ \_____/ |_|  \_| \_____/ 

	            Author: %s && Ver: %s
  	 		     
	""" % ("Bing","2.0")
	print(usage)
	print('Run %s (%s)...' % ("wkengine", os.getpid()) )

	try:
		pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db_result , password = redis_pwd, socket_timeout=3)
		r = redis.Redis(connection_pool=pool)
	except:
		print("Middleware connect fail !!! please try again ...")
		sys.exit(0)

	while True:
		size = r.scard("scan_batch")
		if size > 0 :
			'''
			同时启用4个，扫描服务
			'''
			start = time.time()
			p = Pool(4)
			count = 0
			for line in range(0, 500):
				try :
					data = r.spop("scan_batch")
					target = eval(data)
					p.apply_async(custom_scan, args=(target,))
					count += 1
				except :
					time.sleep(30)
					print("Middleware connect fail !!! please try again ...")

			print("Waiting for %d task done..." % count)
			p.close()
			p.join()
			print("All subprocesses done.")

		else:
			time.sleep(30)
			print("Waiting for task loading ...")





