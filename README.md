# Wukong Scanner Agent v1

[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/Canbing007/wukong-agent)
[![python](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)


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









