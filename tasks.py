# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: celery task 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

from celery import Celery, platforms 
from datetime import timedelta
from celery.schedules import crontab

import time,subprocess,sys
from core.settings import *

app = Celery()
platforms.C_FORCE_ROOT = True

app.conf.update(
    CELERY_IMPORTS = ("tasks", ),
    BROKER_URL = 'redis://'+':'+ redis_pwd + '@'+ redis_host +':'+ str(redis_port) +'/0',
    CELERY_RESULT_BACKEND = 'redis://'+':'+ redis_pwd + '@'+ redis_host +':'+ str(redis_port) +'/2',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_REDIS_MAX_CONNECTIONS=5000,
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600},     
)


@app.task
def brute(task_id = "", task_target = "",model = "" , scan_type = "" , cookie = "wukong" , thread_num = 50 ):
    if task_id != "" and task_target != "":
        if scan_type == "":
            cmdline = 'python brute.py -i %s -d %s -m %s -t \"\" -c %s -th %d' % (task_id,task_target,model,cookie,thread_num)
            print cmdline
        else:
            cmdline = 'python brute.py -i %s -d %s -m %s -t %s -c %s -th %d' % (task_id,task_target,model,scan_type,cookie,thread_num)
            print cmdline            
    else:
        pass

    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return "process_output"


@app.task
def awvs(task_id = "" , task_target = "" , cookie = "wukong" ):
    if task_id != "" and task_target != "":
        cmdline = 'python awvs.py -i %s -d %s -c %s' % (task_id,task_target,cookie)
        print cmdline
    else:
        pass
    
    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return "process_output"


@app.task
def nessus(task_id = "", task_target = "" , cookie = "" ):
    if task_id != "" and task_target != "":
        cmdline = 'python nessus.py -i %s -d %s' % (task_id,task_target)
        print cmdline
    else:
        pass
    
    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return "process_output"


@app.task
def pscan(task_id = "", task_target = "" ):
    if task_id != "" and task_target != "":
        cmdline = 'python pscan.py -i %s -d %s' % (task_id,task_target)
        print cmdline
    else:
        pass
    
    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()

    return "process_output"


# print brute(task_id = "sdfsg", task_target = "www.baidu.com",model = "web" , scan_type = "subdomain")
# 