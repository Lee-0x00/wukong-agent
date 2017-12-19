<<<<<<< HEAD
# Wukong Scanner Agent v1

[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/Canbing007/wukong-agent)
[![python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/)


## Structure

![wukong_structure.png](http://upload-images.jianshu.io/upload_images/2693750-90800cae74c39f4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## Requisites

- python3
- redis
- awvs api
- nessus api

## Introduce

- 跨平台运行       
- 可单个插件扫描，也可按流程扫描
- 可单机或者分布式运行         
- 可接入第三方扫描软件    
- 可自定义插件     
- 可自定义多种报告生成形式【目前包含pdf,web；去掉了elk】     
- 包含任务日志记录
- 任务完成自动以PDF形式发送邮件报告；默认关闭状态，需进行配置

## Installation

```
python要求3.0以上版本
1.安装phantomjs
2.安装awvs
3.安装nessus
4.安装依赖库
	pip install -r requirements.txt  
5.安装redis


修改配置文件 "core/setting.py" 里面的各种用户和密码,端口,webapi

例如：

redis_host = 'localhost'    		#redis地址   
redis_port = 6379           		#redis端口   
redis_pwd = ''              		#redis密码

awvs_url : "127.0.0.1" ,    		#awvs的url
awvs_port : 8183 ,          		#awvs的端口

nessus_url : "https://xxx.com" ,    #nessus的url
nessus_name : "xx" ,                #nessus的用户名
nessus_pass : "xx" ,                #nessus的密码

邮件提醒功能：
send_mail(host, pdfname) 		# 在utils文件夹中的api文件配置,去掉前面的注释


```

## Usage 

```
python daemon.py  			# 运行agent守护进程
python send_task.py 		# 发送任务队列，可批量

```


## Custom plug-in

```
# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

import socket
from exploit.module.example import WKExploit

class Exploit(WKExploit) :
	def __init__(self, args) :
		'''
		漏洞信息和测试参数
		'''
		self.info = {
			# 输入参数
			"protorl" : self.parameter(args["protorl"],"http://"),
			"host" : self.parameter(args["host"], ""), 
			"port" : self.parameter(args["port"], "6379"),
			"cookie" : self.parameter(args["cookie"], ""),
			"fuzzing" : self.custom_fuzzing_api("brute","redis") ,
		}

		self.result = {
			# 结果信息
			"status" : False,		#默认False为无结果，设置True为有结果
			"data" : [{
				"bug_name" : "redis弱口令",
				"bug_author" : "Bing",
				"bug_level" : self.level.high,
				"bug_type" : self.category.misconfiguration,
				"bug_ref" : "",
				"bug_desc" : "",
				"bug_result" : [],
				"bug_repair" : "修改弱口令，并设置强密码"
			}],
		}

	def check(self, txt):
		'''
		漏洞验证
		'''
		host = self.info["host"]
		port = self.info["port"]
		password = txt

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(2)
			s.connect( (host,int(port)) )
			s.send('INFO\r\n'.encode())
			result = s.recv(1024).__str__()
			if "redis_version" in result:
				self.result["status"] = True
				if "unauthorized" in self.result["data"][0]["bug_result"] :
					pass
				else:
					print(password,"----")
					self.result["data"][0]["bug_result"].append("unauthorized")
			else:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect( (host,int(port)) )
				s.send( ("AUTH %s\r\n" % (password) ).encode() )
				result = s.recv(1024).__str__()
				if '+OK' in result:
					self.result["status"] = True
					if password in self.result["data"][0]["bug_result"] :
						pass
					else:
						self.result["data"][0]["bug_result"].append(password)
		except Exception as e:
			pass

```


## Screen 

#### wukong web server[add task page]

![web server](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/scantask.png)  
![web server](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/scantask1.png)  
![local control](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/console.png) 

#### wukong web server[task report page]  

![web server](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/report.png)  
![web server](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/report1.png)  

#### local pdf report  

![pdf report](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/report2.png)  

#### mail function  

![mail report](https://raw.githubusercontent.com/Canbing007/wukong-agent/master/screen/mail.png)  


## Contribute

If you want to contribute to my project please don't hesitate to send a pull request. You can also join our users, by sending an email to [me](mailto:wulitouhaha@vip.qq.com), to ask questions and participate in discussions.


## Issue

if you hava some question or good idea,you can leave a message to me!









=======
# Wukong Scanner Agent v1

[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/Canbing007/wukong-agent)
[![python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/)


## Structure

![wukong_structure.png](http://upload-images.jianshu.io/upload_images/2693750-90800cae74c39f4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## Requisites   
python3.6
redis  
nessus  
awvs  
sqlmap

## Introduce

- Cross platform         
- Single machine can also be distributed         
- Access to third party scannning software   
- Custom plugins        
- Reports can genrate any formats that follow you     
- Include program log and system log


## Installation

```
pip install -r requirements.txt  

Modify "core/setting.py" as following:

redis_host = 'localhost'    		#redis address   
redis_port = 6379           		#redis port   
redis_pwd = ''              		#redis password

awvs_url : "127.0.0.1" ,    		#awvs url
awvs_port : 8183 ,          		#awvs port

nessus_url : "https://xxx.com" ,    #nessus url
nessus_name : "xx" ,                #nessus username
nessus_pass : "xx" ,                #nessus passowrd

```

## Usage 

```
redis-server				#start redis
python2.7 sqlmapapi.py -s 	#start sqlmap
python engine.py  			#start engine

then, waiting for scan task queue into redis ...  

测试样本:
1.搭建sql注入服务站点，先导入screen目录下的tt.sql数据库
2.安装flask,运行screen目录下存在注入的flask-test.py 小型web服务  
python flask-test.py
3.模拟写入一条测试sqlmap的数据，修改screen目录下test.py的redis配置，然后运行

测试步骤如下：


#提示：windows下并发有线程限制不能超过1024, 如果则linux下任务，可以修改engine.py下每个模块的线程数
#服务端页面有点low,暂不公布源码；有继续研究的，可以自己写个简单服务端
```

#### 服务端功能界面    




## Custom plug-in

```
# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

from utils.exploit import *
import socket, re, gevent
from gevent.pool import Pool
from gevent import monkey; monkey.patch_all()


class wk(object):
    def __init__(self, target = None ):
        self.info = {
            # 输入参数
            "protorl" : target["scan_protorl"],
            "host" : target["scan_target"],    
            "port" : target["scan_port"],
            "cookie" : target["scan_cookie"],
            "proxy" : target["scan_proxy"],
            "user_agent" : random_useragent(target["scan_user_agent"]),
            "fuzzing" : target["fuzzing"]
            #{"user": "" ,"pwd" : "", "brute_char" : ""} 
        }
        self.result = [{
            # 结果信息
            "status" : False,
            "data" : {
                "bug_name" : "",
                "bug_author" : "Bing",
                "bug_level" : normal,
                "bug_type" : other,
                "bug_ref" : "",
                "bug_desc" : "",
                "bug_result" : "",
                "bug_repair" : ""
            },
        }]


    def get_port_service(self, content):
        REGEX = [['ssh','^b\'SSH'],['ftp','^b\'220.*?ftp|^b\'220-|^b\'220 Service|^b\'220 FileZilla'],['telnet','^b\'\\xff[\\xfa-\\xfe]|^b\'\\x54\\x65\\x6c|Telnet'],['http','http'],['mysql','^b\'.\\0\\0\\0.*?mysql|^b\'.\\0\\0\\0\\n|.*?MariaDB server'],['redis','-ERR|^b\'\\$\\d+\\r\\nredis_version'],['memcached', '11211', '^b\'ERROR']]
        for info in REGEX:
            name = info[0]
            reg = info[1]
            matchObj = re.search(reg, content, re.I|re.M)
            if matchObj:
                return name
        return "None"


    def exploit(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        host = self.info["host"]
        port = int(self.info["fuzzing"]["brute_char"])
        address = (host, port)

        try:
            sock.connect(address)
            sock.send("OPTION ／ HTTP 1.1\r\n".encode())
            text = sock.recv(256)
            buffers = """{}""".format(str(text.__str__()[0:200]))
            finger = self.get_port_service(buffers)

            bug_list = {}
            bug = {
                "bug_name" : finger,
                "bug_author" : "Bing",
                "bug_level" : normal,
                "bug_type" : other,
                "bug_ref" : "",
                "bug_desc" : buffers,
                "bug_result" : port,
                "bug_repair" : ""
            }
            bug_list["status"] = True
            bug_list["data"] = bug
            self.result.append(bug_list)
        except Exception as e:
            sock.close()
        sock.close()


info = {
    'scan_taskid': '3', 
    'scan_protorl': 'http://', 
    'scan_target': 'xx.xx.com', 
    'scan_port': '80', 
    'scan_cookie': 'sdf', 
    'scan_proxy': 'sdf', 
    'scan_user_agent': True, 
    'plugin_name': '端口扫描', 
    'plugin_file': 'plugins/wk-174745431967-00.py', 
    'model': 'brute', 
    'fuzzing': {'user_pwd': '', 'brute_char': '80'}
}
t = wk(info)
t.exploit()
print(t.result)

```

## Contribute

If you want to contribute to my project please don't hesitate to send a pull request. You can also join our users, by sending an email to [me](mailto:wulitouhaha@vip.qq.com), to ask questions and participate in discussions.


## Issue

Notice:    
everything in here that just for fun ...   
if you hava some question or good idea,you can leave a message to me!





>>>>>>> wk agent v2
