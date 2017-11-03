# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_PATH = os.path.join(BASE_PATH,"exploit")
DICT_PATH = os.path.join(BASE_PATH,"dictionary")

#消息中间件
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = ''
redis_db_result = 1
redis_db_log = 3


#wk 控制台API
login_url = 'http://localhost:8088/login/'
result_url = 'http://localhost:8088/scanner/report/'
log_url = 'http://localhost:8088/scanner/task/'

#默认的日志账号
user_pwd = {'username':'xx','password':'xx' }


#第三方工具配置
awvs_urls = "127.0.0.1" 
awvs_ports = 8183

nessus_urls = "https://xx.xx"
nessus_names = "xx"
nessus_passs = "xxx"

#第三方报告目录
TMEP_REPORT_PATH = os.path.join(BASE_PATH,"report")


#邮箱设置
EMAIL_HOST = "smtp.163.com"					#定义发送邮件服务器
EMAIL_PORT = 25
EMAIL_HOST_USER = "xx"
EMAIL_HOST_PASSWORD = "xx"
EMAIL_USE_TLS= False
EMAIL_TO = ";".join(['xx@xx.com'])
