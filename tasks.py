# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: celery task 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import time
from celery import Celery, platforms 
from datetime import timedelta
from celery.schedules import crontab

import smtplib
from email.mime.text import MIMEText
from core.settings import *

from libraries.github import run as github
from libraries.web import Work as Web
from libraries.pscan import Work as Pscan
from libraries.brute import Work as Brute
from libraries.awvs import Work as Awvs
from libraries.nessus import Work as Nessus
    
#from multiprocessing import Pool,Process
#import gevent

app = Celery()
platforms.C_FORCE_ROOT = True

app.conf.update(
    CELERY_IMPORTS = ("tasks", ),
    BROKER_URL = 'redis://127.0.0.1:6379/0',
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_REDIS_MAX_CONNECTIONS=5000, 
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600},    
    # BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True},       
#	CELERYBEAT_SCHEDULE = {
#	'add-every-30-seconds': {
#	   'task': 'tasks.mail_notify',
#	   'schedule': timedelta(seconds=10),
#	   'args': ("test","Talscan Notice !!! ")      
#	},
#	# 'add-every-monday-morning': {
#	#   'task': 'tasks.add',
#	#   'schedule': crontab(hour=1, minute=16, day_of_week=4),
#	#   'args': (40, 30),
#	# },
#	}
)



@app.task
def custom_poc_scan(taskid = "" , host = "" , args = ""):
	'''
	args 为扫描POC的类型；参数可以是数组，也可以是字符 如：args = "subdomain";args = ["subdomain","dnszone"]
	'''
	test = []
	if type(args) == type(test) and len(args) > 0 :
		for scan_type in args :
			t = Web( scan_id = taskid ,scan_target = host,scan_type = scan_type)
			t.run()
	else :
		t = Web( scan_id = taskid ,scan_target = host,scan_type = args)
		t.run()		


@app.task
def custom_brute_scan(taskid = "" , host = "" , args = ""):
	test = []
	if type(args) == type(test) and len(args) > 0 :
		for scan_type in args :
			t = Brute( scan_id = taskid ,scan_target = host,scan_type = scan_type)
			t.run()
	else :
		t = Brute( scan_id = taskid ,scan_target = host,scan_type = args)
		t.run()		



@app.task
def custom_nmap_scan(taskid = "" , host = "" , args = ""):
	t = Pscan( scan_id = taskid ,scan_target = host)
	t.run()		


@app.task
def awvs_scan(taskid = "" , host = "" , args = ""):
	t = Awvs( scan_id = taskid ,scan_target = host)
	t.run()



@app.task
def nessus_scan(taskid = "" , host = "" , args = ""):
	t = Nessus( scan_id = taskid ,scan_target = host)
	t.run()


@app.task
def rsas_scan(taskid = "" , host = "" , args = ""):
	pass



@app.task
def github_scan(taskid = "" ,host = "" ,args = "") :
	github( scan_id = taskid ,scan_target = host ,scan_args = args)

@app.task
def custom_spider_scan(taskid = "" , host = "" , args = {}):
	pass

@app.task
def custom_rule_scan(taskid = "" , host = "" , args = {}):
	pass



#celery -A tasks beat --loglevel=info
#celery beat -A tasks work --loglevel=info
#celery -A tasks work --loglevel=info


# custom_poc_scan(taskid = "taskid-296" ,host = "100.xueersi.com",args = "subdomain")
# custom_brute_scan(taskid = "taskid-296" ,host = "100.xueersi.com",args = "subdomain")
# custom_nmap_scan(taskid = "taskid-296" ,host = "www.baidu.com",args = "subdomain")
# awvs_scan(taskid = "taskid-296" ,host = "100.xueersi.com")
# nessus_scan(taskid = "taskid-296" ,host = "100.xueersi.com")
# github_scan(taskid = "taskid-296" ,host = "100.xueersi.com" ,args = ["email"])
