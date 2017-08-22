# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: configure 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import redis

# **************************************************database configure********************************************************************

redis_host = 'localhost'
redis_port = 6379
redis_pwd = ''
redis_db_result = 1

def save_result(save_key,save_value):
	try:
		task_redis = redis.ConnectionPool(host = redis_host,port = redis_port,db = redis_db_result ,password = redis_pwd,socket_timeout=3)
		redis_task = redis.Redis(connection_pool = task_redis)
		redis_task.sadd("{0}".format(save_key),save_value)
		return True
	except:
		return False


# **************************************************path configure********************************************************************

BASE_PATH = "M:\\work\\sec platform\\wukong_agent\\"


PLUGIN_PATH = BASE_PATH + "plugins\\"
DICT_PATH = BASE_PATH + "dictionary\\"
SCAN_PATH = BASE_PATH + "lib\\"
TMEP_REPORT_PATH = BASE_PATH + "report\\"
AWVS_COOKIE_FILE = "C:\\Users\\Public\\Documents\\Acunetix WVS 10\\LoginSequences"


#**************************************************其他配置项********************************************************************

talscan_config = {
	#mail
	"mail_host" : "smtp.163.com", 
	"mail_user" : "xx",
	"mail_pass" : "xx",
	"mail_postfix" : "163.com",

	#request
	"allow_ssl_verify" : False ,
	"timeout" : 5 ,
	"allow_redirects" : True ,
	"allow_http_session" : True ,
	"allow_random_useragent" : False ,
	"allow_random_x_forward" : False ,
	"proxies" : {
		# "http": "http://user:pass@xx:3128/",
		# "https": "http://xx:1080",
		# "http": "http://xx:xx", # TOR
	},
	"custom_cookie" : "whois=wukong",

	#report
	"report_filters" : {
		"awvs_white_list": ["orange", "red", "blue" ],	# green,blue,orange,red
		"nessus_white_list": ["High", "Medium","Low"],
		"bug_black_list": [								
			"User credentials are sent in clear text"
		]
	} ,
	"report_save_dir" : TMEP_REPORT_PATH ,

	#third configure
	"loginseq_dir" : AWVS_COOKIE_FILE ,
	"awvs_url" : "127.0.0.1" ,
	"awvs_port" : 8183 ,
	"awvs_header" : {
			"Content-Type": "application/json; charset=UTF-8",
			"X-Requested-With": "XMLHttpRequest",
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"RequestValidated": "true"
	},
	"nessus_url" : "https://xx" ,
	"nessus_name" : "xx" ,
	"nessus_pass" : "xx" ,
	"rsas_host" : "1.1.1.1" ,
	"rsas_name" : "xx" ,
	"rsas_pass" : "xx" 

}








