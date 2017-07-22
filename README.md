悟空扫描器
---  

## Frame  
![悟空架构图](https://raw.githubusercontent.com/Canbing007/wukong/master/wukong.png)  


## Introduce   
```
1.扫描器AGENT端架构:python+flower+celery+redis    
2.目前主要模块:   
awvs：["taskid-23","www.baidu.com"]   
nessus：["taskid-23","www.baidu.com"]   
爆破：["taskid-23","www.baidu.com"]		 		目前仅redis可自己添加其他插件    
POC：["taskid-23","www.baidu.com","插件名称"]   
端口：["taskid-23","www.baidu.com"]   

3.可自定义添加在爆破和POC模块添加插件；插件模块设置见下面描述    
4.可分布式部署  
5.可接入第三方扫描工具  
6.跨平台运行
```

## libraries(安装工具)

```
apt-get -y install dnsutils  
apt-get -y install phantomjs  
apt-get install -y net-tools  
apt-get -y install python
apt-get -y install redis-server  
apt-get install -y -q python-pip  

pip install -r requirements.txt
pip install celery
pip install flower
pip install supervisor

* windows下celery 必须是3版本，flower必须下载安装
pip install celery==3.1.25

* Mac使用requests请求htpps链接时，返回错误或延长时间；需要安装
pip install --upgrade ndg-httpsclient


```

## Dir list(目录结构)  
```
│  tasks.py 						#celery任务文件
│  __init__.py
│
├─common
│      captcha.py 					#获取验证码为文件
│      wukong_Func.py 				#公共函数调用
│      wukong_TypeCheck.py 			#数据格式验证
│      __init__.py
│
├─core
│      settings.py 					#主要配置文件
│      __init__.py
│
├─dictionary
│      brute-qqmail.txt 			#qqmail爆破字典
│      brute-redis.txt 				#redis爆破字典
│      brute-subdomain.txt 			#子域名爆破字典
│      nmap-services.txt 			#nmap端口指纹
│      __init__.py
│
├─libraries
│      awvs.py 						#awvs主程序
│      brute.py 					#爆破主程序; todo:待修改获取参数接口，添加一个获取参数功能
│      github.py 					#github泄露搜索主程序
│      nessus.py 					#nessus主程序
│      pscan.py                     #端口扫描主程序
│      web.py 						#通用型poc扫描住程序
│      __init__.py
│
└─plugins
        brute_qqmail_20170713.py 	#qqmail爆破插件
        brute_redis_20170713.py     #redis爆破插件
        brute_subdomain_12532324.py
        web_dnszonetransfer_12531324.py #通用型DNS区域传送漏洞插件
        web_subdomain-20170620.py       #通用型子域名httpapi插件
        web_subdomain-20170627.py

```

## Plugins(插件编写)

```
#!/user/bin python
# -*- coding:utf-8 -*- 
# Author: 作者
# Contact: xx@outlook.com
# DateTime: 2016-12-21 11:46:49
# Description:  coding 

import sys
sys.path.append("..")

from common.captcha import Captcha    #验证码功能
from common.wukong_Func import *      #通用功能
from common.wukong_TypeCheck import * #格式验证功能

class WuKong(object):
    def __init__(self,  target = ""):
        self.target = target
        self.website = "https://www.threatminer.org"
        self.result = {
        "bug_author" : "作者",
        "bug_name" : "POC名称",
        "bug_summary" : "POC简介", 
        "bug_level" : "危害等级" , 
        "bug_detail" : [] ,
        "bug_repair" : "修复建议"
        }
    
    def run(self):
        if is_domain(self.target) == False :
            return []

        target = str(".".join(self.target.split(".")[1:]))
        try:
            url = "{0}/getData.php?e=subdomains_container&q={1}&t=0&rt=10&p=1".format(self.website, target )
            content = http_request_get(url).content

            _regex = re.compile(r'(?<=<a href\="domain.php\?q=).*?(?=">)')
            for sub in _regex.findall(content):
                if is_domain(sub):
                    self.result["bug_detail"].append(sub) 	#保存结果

            return list(set(self.result))
        except Exception as e:
            return 0

```



## Usage(使用方式)
```
- 配置supervisor的启动项
- 修改core/settings.py 文件配置信息

agent端运行以下命令:
celery flower --port=8080 --broker=redis://127.0.0.1:6379/0 --basic_auth=talsec:talsec@flower
celery -A tasks worker --loglevel=info --workdir=/root/test --concurrency=10


docker 运行方式:
docker run -d -v /mnt/:/tmp/ -p 222:22 -p 6379:6379 -p 9001:9001 -p 8080:8080 wukong


必须设置一个启动supervisord的脚本；并配置supervisord
/tmp/Run.sh
#!/bin/bash
supervisord -c '/tmp/supervisord_server.conf'

如果想自定义启动的agent和redis可修改supervisord_server 配置




提交任务扫描请求:
curl -X POST -d '{"args":["taskid-23","www.baidu.com","test"]}' http://192.168.10.128:8080/api/task/send-task/tasks.custom_nmap_scan

curl -X POST -d '{"args":["taskid-296","100.xueersi.com","subdomain"]}' http://192.168.10.128:8080/api/task/send-task/tasks.custom_poc_scan

curl -X POST -d '{"args":["taskid-296","100.xueersi.com","subdomain"]}' http://192.168.10.128:8080/api/task/send-task/tasks.custom_brute_scan

curl -X POST -d '{"args":["taskid-296","100.xueersi.com"]}' http://192.168.10.128:8080/api/task/send-task/tasks.nessus_scan

curl -X POST -d '{"args":["taskid-296","100.xueersi.com",["email"]]}' http://192.168.10.128:8080/api/task/send-task/tasks.github_scan

curl -X POST -d '{"args":["taskid-23","100.xueersi.com"]}' http://192.168.10.128:8080/api/task/send-task/tasks.awvs_scan

强制结束一个正在执行的任务：
curl -X POST -d 'terminate=True' http://192.168.10.128:8080/api/task/revoke/a9361c1b-fd1d-4f48-9be2-8656a57e906b


```


## Todo
1.待编写web服务端   
2.爆破模款(字典配置)和poc模块(cookie设置)调整




