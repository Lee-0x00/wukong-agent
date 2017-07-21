# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: usually function(public)
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys,os
sys.path.append("..")

#import gevent,time
#from gevent import monkey
#from gevent.pool import Pool
#monkey.patch_all()
import threading, socket, sys, cmd, os, Queue
import imp,random

from core.settings import redis_task
from common.wukong_Func import get_web_poc,get_dict

lock = threading.Lock()
def GetQueue(host,poc_list):
	PortQueue = Queue.Queue()
	for poc in poc_list :
		poc_args = get_dict(poc)	#什么样的poc,获取什么样的字典;例如：从api获取args:[{"username":"test","passwd":"sdf"},{"username":"test","passwd":"sdf"}]
		for args in poc_args :
			PortQueue.put((host,poc,args))
	return PortQueue

class ScanThread(threading.Thread):
    def __init__(self,TaskQueue,OutQueue):
        threading.Thread.__init__(self)
        self.setDaemon(True)		#后台运行
        self.TaskQueue = TaskQueue
        self.OutQueue = OutQueue

    def excute(self,host, poc_path,poc_args):
		global lock
		try:
			poc_class = imp.load_source('WuKong', poc_path)
			wukong = poc_class.WuKong(target = host , args = poc_args)
			wukong.run()
			lock.acquire()
			self.OutQueue.put(wukong.result)
			lock.release()
		except :
			print "类调用失败"
			return False			


    def run(self):
		while not self.TaskQueue.empty():
			host,poc_path,poc_args = self.TaskQueue.get()
			self.excute(host,poc_path,poc_args)


class Work(object):
	def __init__(self, scan_id = "", scan_target = "", scan_type = "" ,scan_args = "", back_fn = None):
		self.scan_id = scan_id
		self.target = scan_target
		self.scan_type = scan_type
		self.args = scan_args
		self.back_fn = back_fn
		self.result = []        


	def run(self):
		ThreadList = []
		poc_list = get_web_poc("brute",self.scan_type)	#查找子域名类型的爆破POC
		#print poc_list

		if len(poc_list) > 0:
			#任务队列
			TaskQueue = GetQueue(self.target,poc_list)

			#结果队列
			resultQueue = Queue.Queue()

			#fork出20个线程
			for i in range(0, 50):
				t = ScanThread(TaskQueue,resultQueue)
				ThreadList.append(t)
			for t in ThreadList:
				t.start()

			if "qqmail" == str(self.scan_type) :
				for t in ThreadList:
					t.join(50)
			else:
				for t in ThreadList:
					t.join(5)	

			data = {}
			while not resultQueue.empty():
				result = resultQueue.get() 
				#result为字典,默认result["bug_detail"]返回的结果都为数组
				if len(result["bug_detail"]) > 0 :
					for line in result["bug_detail"] :
						data["scan_id"] = self.scan_id 
						data["model"] = "web"
						data["scan_type"] = self.scan_type
						data["bug_author"] = result["bug_author"]
						data["bug_name"] = result["bug_name"]
						data["bug_summary"] = result["bug_summary"]
						data["bug_level"] = result["bug_level"]
						data["bug_detail"] = line
						data["bug_repair"] = result["bug_repair"]
						#self.back_fn(result) 回掉给api

						redis_task.sadd("brute_result",data)
						print data
			#任务最终结束
			final_result = { "status" : 1 , "scan_id": self.scan_id , "model": "brute" }

			redis_task.sadd("brute_result",final_result)
			print final_result


# t = Work( scan_id = "taskid-233" ,scan_target = "www.nknu.edu.tw",scan_type = "subdomain")
# t = Work( scan_id = "taskid-233" ,scan_target = "www.tiandaoedu.com",scan_type = "qqmail")	#qqmail的Browser 默认使用线程不能调用
# t = Work( scan_id = "taskid-233" ,scan_target = "127.0.0.1",scan_type = "redis")
# t.run()

