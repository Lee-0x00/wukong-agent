# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39

import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_PATH = os.path.join(BASE_PATH,"plugins")
DICT_PATH = os.path.join(BASE_PATH,"dictionary")
TMEP_REPORT_PATH = os.path.join(BASE_PATH,"report")

#消息中间件&缓存日志和结果
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = ''
redis_db_task = 1

#wk 控制台API
API_REPORT_URL = "http://localhost:8888/scan/report/api/"
API_LOG_URL = "http://localhost:8888/scan/log/api/"

#--------------------- 第三方配置 -----------------------------
nessus_url = "https://xxx.com"
nessus_name = "xxx"
nessus_pass = "xxx"

awvs_url = "127.0.0.1" 
awvs_port = 8183
awvs_header = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "RequestValidated": "true"
}


report_filter =  {
    "awvs_white_list": ["orange", "red", "blue" ],  # green,blue,orange,red
    "nessus_white_list": ["High", "Medium","Low", "Info"],
    "bug_black_list": [                             
        "User credentials are sent in clear text"
    ]
} 


















