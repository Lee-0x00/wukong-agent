# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: usually function(public)
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys,os
sys.path.append("..")

import argparse,logging
import threading,Queue,imp

from common.func import get_web_poc,get_brute_dict 			#verify_format
from core.settings import save_result 						#configure
  

lock = threading.Lock()

def GetQueue(host = '' , poc_list = '' , cookie = ''):
	PortQueue = Queue.Queue()

	for poc_file in poc_list :
		dict_list = get_brute_dict(poc_file)

		if len(dict_list) > 0 :
			a = ()
			if type(dict_list[0]) == type(a) :
				for args in dict_list :
					#args:("user":"pass")
					poc_args = { "cookies": cookie , "user_pass": args , "args" : "" }
					PortQueue.put( (host,poc_file,poc_args) )
			else:
				for args in dict_list :
					#args: poc_args .for example: 2.php/www/dicuz1x
					poc_args = { "cookies": cookie , "user_pass": "" , "args" : args }
					PortQueue.put( (host,poc_file,poc_args) )
		else:
			poc_args = { "cookies":"" , "user_pass": "" , "args" : "" }
			#print poc_args
			PortQueue.put( (host,poc_file,poc_args) )
					
	return PortQueue

class ScanThread(threading.Thread):
	def __init__(self,TaskQueue,OutQueue):
		threading.Thread.__init__(self)
		self.setDaemon(True)		#backend running
		self.TaskQueue = TaskQueue
		self.OutQueue = OutQueue

	def excute(self,host, poc_file,poc_args):
		global lock
		try:
			poc_class = imp.load_source('WuKong', poc_file )
			wukong = poc_class.WuKong(target = host , args = poc_args)
			wukong.exploit()
			
			lock.acquire()
			self.OutQueue.put(wukong.result)
			lock.release()
		except :
			logging.error("call class fail")
			return False			

	def run(self):
		while not self.TaskQueue.empty():
			host , poc_file , poc_args = self.TaskQueue.get()
			self.excute(host , poc_file , poc_args)



class Work(object):
	def __init__(self, task_id = "", task_target = "", model = "" , cookie = "" , scan_type = "" , thread_num = 50 ):
		self.task_id = task_id
		self.task_target = task_target
		self.model = model
		self.scan_type = scan_type
		self.cookie = cookie
		self.thread_num = int(thread_num)
		self.result = []  

	def run(self):
		ThreadList = []
		poc_list = get_web_poc(self.model,self.scan_type)

		if len(poc_list) > 0:
			#task queue
			TaskQueue = GetQueue(host = self.task_target , poc_list = poc_list , cookie = self.cookie)

			#result queue
			resultQueue = Queue.Queue()

			#fork 20 threading
			for i in range(0, self.thread_num):
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


			while not resultQueue.empty():
				result = resultQueue.get() 
				if len(result["bug_detail"]) > 0 :
					for line in result["bug_detail"] :					
						task_result = {
							"task_id": self.task_id ,
							"bug_model": self.model ,
							"bug_type" : self.scan_type ,
							"bug_author" : result["bug_author"] ,
							"bug_name" : result["bug_name"] ,
							"bug_level" : result["bug_level"],
							"bug_summary" : result["bug_summary"] ,
							"bug_detail" : line ,
							"bug_repair" : result["bug_repair"]
						}

						save_result(self.model,task_result)
						self.result.append(task_result)

			#finish
			final_result = { "status" : 1 , "task_id": self.task_id , "bug_model": self.model }
			save_result(self.model,final_result)
			self.result.append(final_result)


if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description="wukong scanner v 1.0")
    parser.add_argument("-i", "--id",metavar="", default='', help="TASKID-20170817-783554")
    parser.add_argument("-d", "--host",metavar="", default='', help="www.x.com/127.0.0.1")
    parser.add_argument("-m", "--model",metavar="", default='', help="web/brute")
    parser.add_argument("-t", "--type",metavar="", default='', help="subdomain")
    parser.add_argument("-c", "--cookie",metavar="", default='', help="SESSIONID=2H23I2Y2K3YI234H")
    parser.add_argument("-th", "--thread",metavar="", default=50, help="50")
    args = parser.parse_args()

    taskid = args.id
    host = args.host
    model = args.model
    scantype = args.type
    cookie = args.cookie
    threadnum = args.thread

    # print taskid,host,model,scantype,cookie,threadnum
    if host != "" :
        try:
            t = Work(task_id = taskid , task_target = host ,model = model , scan_type = scantype , cookie = cookie , thread_num = threadnum )
            t.run()
            for line in t.result :
                print line
        except:
            print parser.print_help()
            sys.exit(1)
    else:
        print parser.print_help()
        sys.exit(1)




