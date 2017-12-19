#!/usr/bin/env python
# coding: utf-8

import redis,datetime, cgi,time,time, random,re

redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = ''
redis_db_result = 1
redis_db_log = 3

pool = redis.ConnectionPool(host = redis_host, port = redis_port, db = redis_db_result , password = redis_pwd, socket_timeout=3)
r = redis.Redis(connection_pool=pool)

info = {
    'scan_taskid': '3', 
    'scan_protorl': 'http://', 
    'scan_target': 'localhost', 
    'scan_port': '5000', 
    'scan_cookie': 'sdf', 
    'scan_proxy': 'sdf', 
    'scan_user_agent': True, 
    'plugin_name': 'sqlmap', 
    'plugin_file': 'plugins/wk-sqlmap-00.py', 
    'model': 'brute', 
    'fuzzing': {'user_pwd': '', 'brute_char': {"method":"POST", "url":"http://localhost:5000/test", "referer":"", "data":"name=tes*"}
    }
}
r.sadd("brute", info)


