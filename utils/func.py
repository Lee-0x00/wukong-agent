# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39
import sys
sys.path.append("..")

from core.settings import * 
import re, os, redis, socket, time, requests


try:
	pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db_task , password = redis_pwd, socket_timeout=3)
	r = redis.Redis(connection_pool=pool)
except:
	pass


def program_log(datas):
	msg = False
	web_info = ""
	try:
		res = requests.post(url = API_LOG_URL, data = datas)
		text = res.status_code
		if int(text) == 200:
			web_info = "日志上传成功"
			msg = True
	except Exception as e:
		web_info = e.__str__()
		msg = False

	if not msg :
		datas["ctime"] = int(time.time())
		datas["nodeip"] = str(socket.gethostbyname(socket.gethostname()))
		try :
			r.sadd("scan_log", datas)
		except Exception as e:
			#进入本地保存
			result_text = "{0}/{1}_log.txt".format(TMEP_REPORT_PATH, datas["taskid"])
			result = open(result_text,"a+")
			html = datas.__str__() + str(e.__str__())
			result.write( html )
			result.write("\n")
			result.close()
		return True
	else:
		return True


def system_log(datas):
	datas["nodeip"] = str(socket.gethostbyname(socket.gethostname()))

	try :
		r.sadd("system_log", datas)
	except Exception as e:
		#进入本地保存
		result_text = "{0}/{1}_systemlog.txt".format(TMEP_REPORT_PATH, datas["model"])
		result = open(result_text,"a+")
		html = datas.__str__() + str(e.__str__())
		result.write( html )
		result.write("\n")
		result.close()

	return True


def program_result(taskid, host, model, plugin_name, result):
	if len(result) > 0:
		for line in result :
			status = line["status"]
			if status:
				datas = line["data"]
				datas["taskid"] = taskid
				datas["host"] = host
				datas["model"] = model
				datas["plugin_name"] = plugin_name
				
				msg = False
				web_info = ""
				try:
					res = requests.post(url = API_REPORT_URL, data = datas)
					text = res.status_code
					if int(text) == 200:
						web_info = "结果上传成功"
						msg = True
				except Exception as e:
					web_info = e.__str__()
					msg = False

				if not msg :
					try:
						r.sadd("scan_result", datas)
						program_log({
							"taskid" : taskid, 
							"model" : model, 
							"plugin_name" : plugin_name, 
							"status" : 1, 
							"info" : "poc redis result ok"
						})
					except Exception as e:
						#进入本地保存
						result_text = "{0}/{1}_log.txt".format(TMEP_REPORT_PATH, result["taskid"])
						local_result = open(result_text,"a+")
						html = result.__str__() + str(e.__str__())
						local_result.write( html )
						local_result.write("\n")
						local_result.close()
						program_log({
							"taskid" : taskid, 
							"model" : model, 
							"plugin_name" : plugin_name, 
							"status" : 1, 
							"info" : "poc local result ok"
						})
				else:
					program_log({
						"taskid" : taskid, 
						"model" : model, 
						"plugin_name" : plugin_name, 
						"status" : 1, 
						"info" : "poc web result ok"
					})
	else:
		return True


def get_task(scan_model,task_num = 5):
	#获取扫描任务
	pid = os.getpid()
	task_que = []
	try :
		for line in list(range(0,task_num)) :
			data = r.spop("{0}".format(scan_model))
			target = eval(data)
			task_que.append(target)
	except Exception as e:
		pass

	return task_que
	

def get_poc_path(scan_poc): 
	#获取插件绝对路径
	plugin_files = os.listdir(PLUGIN_PATH)
	regex = re.compile('^(wk-).*?' + scan_poc + '.*?\.py$')

	for poc_file in plugin_files:
		match = regex.search(poc_file) 
		if match :
			return str(os.path.join(PLUGIN_PATH, poc_file))

	return False
