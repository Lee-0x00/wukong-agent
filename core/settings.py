# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: configure 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import redis

#**************************************************数据库配置项********************************************************************

redis_host = 'localhost'
redis_port = 6379
redis_pwd = ''
redis_db_result = 1

task_redis = redis.ConnectionPool(host = redis_host,port = redis_port,db = redis_db_result ,password = redis_pwd) 
redis_task = redis.Redis(connection_pool = task_redis)


#**************************************************其他配置项********************************************************************

talscan_windows_config = {
	#邮箱配置
	"mail_host" : "smtp.163.com", 
	"mail_user" : "xx",
	"mail_pass" : "xx",
	"mail_postfix" : "163.com",
	#request配置d
	"allow_ssl_verify" : False ,
	"timeout" : 5 ,
	"allow_redirects" : True ,
	"allow_http_session" : True ,
	"allow_random_useragent" : False ,
	"allow_random_x_forward" : False ,
	"proxies" : {
		# "http": "http://user:pass@10.10.1.10:3128/",
		# "https": "http://10.10.1.10:1080",
		# "http": "http://127.0.0.1:8118", # TOR
	},
	"custom_cookie" : "whois=wukong",

	#报告配置
	"report_filters" : {
		"awvs_white_list": ["orange", "red", "blue" ],	# green,blue,orange,red四种级别
		"nessus_white_list": ["High", "Medium","Low"],
		"bug_black_list": [								# 漏洞黑名单，过滤掉一些危害等级高，但没什么卵用的洞
			"User credentials are sent in clear text"
		]
	} ,
	"report_save_dir" : "M:\\awvs\\" ,

	#其他第三方配置
	"loginseq_dir" : "C:\\Users\\Public\\Documents\\Acunetix WVS 10\\LoginSequences" ,
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

talscan_linux_config = {
	#邮箱配置
	"mail_host" : "smtp.163.com", 
	"mail_user" : "xx",
	"mail_pass" : "xx",
	"mail_postfix" : "x.com",
	#request配置d
	"allow_ssl_verify" : False ,
	"timeout" : 5 ,
	"allow_redirects" : True ,
	"allow_http_session" : True ,
	"allow_random_useragent" : False ,
	"allow_random_x_forward" : False ,
	"proxies" : {
		# "http": "http://user:pass@10.10.1.10:3128/",
		# "https": "http://10.10.1.10:1080",
		# "http": "http://127.0.0.1:8118", # TOR
	},
	"custom_cookie" : "whois=wukong",

	#报告配置
	"report_filters" : {
		"awvs_white_list": ["orange", "red", "blue" ],	# green,blue,orange,red四种级别
		"nessus_white_list": ["High", "Medium","Low"],
		"bug_black_list": [								# 漏洞黑名单，过滤掉一些危害等级高，但没什么卵用的洞
			"User credentials are sent in clear text"
		]
	} ,
	"report_save_dir" : "/tmp/" ,

	#其他第三方配置
	"loginseq_dir" : "C:\\Users\\Public\\Documents\\Acunetix WVS 10\\LoginSequences" ,
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

# POC_PATH = "/AGENT目录下的插件目录/plugins/"
# dict_script_path = "/AGENT目录下的字典目录/dictionary/"
talscan_config = talscan_windows_config



# POC_PATH = "/AGENT目录下的插件目录/plugins/"
# dict_script_path = "/AGENT目录下的字典目录/dictionary/"
# talscan_config = talscan_linux_config





