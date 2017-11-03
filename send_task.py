# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

from core.settings import *
from time import sleep
import redis, json, random, argparse, time


def HashId(prefix):
	'''
	生成任务ID
	'''
	times = time.strftime("%Y%m%d", time.localtime())
	test = ""
	for i in range(0,6):
	    test += str(random.randint(0,9))
	result = prefix +"-"+ str(times)+"-{0}".format(test)
	return result


def batch_task(text):
	'''
	批量添加任务
	'''
	pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db_result , password = redis_pwd, socket_timeout=3)
	r = redis.Redis(connection_pool=pool)

	count = 0 
	f = open("{0}".format(text), 'r')
	for line in f.readlines():
		#任务参数
		taskid = HashId("TASKID")
		domain = line.strip()

		data = {'taskid' : taskid , 'cookie' : 'wukong', 'plugins' : 'all','host' : domain}
		r.sadd("scan_batch", data)
		count += 1
	f.close()
	print("已添加 %d个任务到redis扫描队列 !" % count) 


if __name__ == '__main__':
	usage = """
	_          __  _   _   _   _    _____   __   _   _____  
	| |        / / | | | | | | / /  /  _  \ |  \ | | /  ___| 
	| |  __   / /  | | | | | |/ /   | | | | |   \| | | |     
	| | /  | / /   | | | | | |\ \   | | | | | |\   | | |  _  
	| |/   |/ /    | |_| | | | \ \  | |_| | | | \  | | |_| | 
	|___/|___/     \_____/ |_|  \_\ \_____/ |_|  \_| \_____/ 

	            Author: %s && Ver: %s
  	 		     
	""" % ("Bing","2.0")


	parser = argparse.ArgumentParser(description="wukong scanner v 2.0")
	parser.add_argument("-f", "--filename",metavar="", default='', help="domain.txt")
	args = parser.parse_args()

	text = args.filename


	if text != "" :
		batch_task(text)
	else:
		print(usage)
		print(parser.print_help())




