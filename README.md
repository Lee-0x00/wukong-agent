# Wukong Scanner Agent v1

[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/Canbing007/wukong-agent)
[![python](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)

## Requisites

- python
- redis
- awvs api
- nessus api

## Structure

![wukong_structure.png](http://upload-images.jianshu.io/upload_images/2693750-90800cae74c39f4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## Introduce

- system structure : python + flower + celery + redis   
- Cross platform operation
- The current module as the following :   
	- awvs : Awvs scanner
	- nessus :  Nessus scanner  
	- brute :  System service account password burst test    
	- web : System web service vulnerability test   
	- pscan : Port scans
- Custom plug-in  
- It can distributed deployment  
- It access to third-party scanning tools


## Installation

modify setting.py as the following
```
redis_host = 'localhost'	#your redis address
redis_port = 6379			#your redis port
redis_pwd = ''				#your redis password

"awvs_url" : "127.0.0.1" ,  #your awvs host
"awvs_port" : 8183 ,		#your awvs password

"nessus_url" : "https://xxx.com" ,	#your nessus host
"nessus_name" : "xx" ,			#your nessus user
"nessus_pass" : "xx" ,	#your nessus password
```


## Usage

#### runing on the server

```
start server:
    celery -A tasks worker --loglevel=info --concurrency=10
    celery flower --port=8080 --broker=redis://127.0.0.1:6379/0
    #celery flower --port=8080 --broker=redis://:password@127.0.0.1:6379/0
    #celery flower --port=8080 --broker=redis://127.0.0.1:6379/0 --basic_auth=xx:xx

send task:
    curl -X POST -d '{"args":["taskid-23","www.baidu.com"]}' http://127.0.0.1:8080/api/task/send-task/tasks.pscan
    curl -X POST -d '{"args":["taskid-23","www.baidu.com","web"]}' http://127.0.0.1:8080/api/task/send-task/tasks.brute
```

#### runing on the console

```
python wukong.py -d 100.xueersi.com -m pscan    	#port scans
python wukong.py -d 100.xueersi.com -m nessus       #nessus scans
python wukong.py -d 100.xueersi.com -m awvs 		#awvs scans
python wukong.py -d 100.xueersi.com -m web 			#all zero day vulnerability scans 
python wukong.py -d 100.xueersi.com -m brute 		#all brute service vulnerability scans 
python wukong.py -d 100.xueersi.com -m brute -c SESSION=232		#all brute service vulnerability scans by cookie
python wukong.py -d 100.xueersi.com -m web -t subdomain 	#subdomain scans by webapi
python wukong.py -d 100.xueersi.com -m brute -t subdomain 	#subdomain scans by brute
python wukong.py -d 100.xueersi.com -m all 		    #scan all the weaknesses
```

#### running screenshot as the following

wukong agent console

![wukong_console.png](http://upload-images.jianshu.io/upload_images/2693750-2b7f18db8fc5c39c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

wukong web api

![celery.png](http://upload-images.jianshu.io/upload_images/2693750-5f4f3310ff3426b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![flower.png](http://upload-images.jianshu.io/upload_images/2693750-a43c2c1b397703ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![send_task.png](http://upload-images.jianshu.io/upload_images/2693750-4af9c91031a1e071.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![flower_result.png](http://upload-images.jianshu.io/upload_images/2693750-898fd9930788bb3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![wukong_agent_result.png](http://upload-images.jianshu.io/upload_images/2693750-c5f30bbfe23dc2d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## Custom plug-in

```
#!/user/bin python
# -*- coding:utf-8 -*- 
# Author:Bing
# Contact:amazing_bing@outlook.com
# Description:  coding 

import sys
sys.path.append("..")

from common.captcha import Captcha 	# Captcha 
from common.func import * 			# Common function
from common.check import * 			# Common format validation 

import json,re,subprocess,time

class WuKong(object):
	'''
	args = { "cookies": cookie , "user_pass": ( "username" , "password" ) , "args" : "" }
	# cookies : it is your cookie
	# user_pass : it is username and password 
	# args : it could be a path,a subdomain prefix , a WEB fingerprint as  x.php / www / discuz! 2.3x etc ...  depending on your poc type
	'''
    def __init__(self,  target = "", args = ""):  	
        self.target = target
        self.cookies = args["cookies"]
        
        self.website = "https://www.threatminer.org"
        self.result = {
            "bug_author" : "Bing",
            "bug_name" : "Threatminer subdomain api",
            "bug_summary" : "Subdomain search", 
            "bug_level" : "Normal" , 
            "bug_detail" : [] ,
            "bug_repair" : "none"
        }
    
    def exploit(self):
        if is_Domain(self.target) == False :
            return []

        target = str(".".join(self.target.split(".")[1:]))
        try:
            url = "{0}/getData.php?e=subdomains_container&q={1}&t=0&rt=10&p=1".format(self.website, target )
            content = http_request_get(url).content

            _regex = re.compile(r'(?<=<a href\="domain.php\?q=).*?(?=">)')
            for sub in _regex.findall(content):
                if is_Domain(sub):
                    self.result["bug_detail"].append(sub)

            return list(set(self.result))
        except:
            pass

''' local test '''            
# test = WuKong(target ='www.aliyun.com',args = {"cookies":"" , "user_pass": "" , "args" : "www" })
# test.exploit()
# print test.result 

```


## Update

| Python version| Wukong Agent version | Link |
| :---:         | :---:          | :--: |
| 2.7.3  		| 1.0  			 | [v1](https://github.com/Canbing007/wukong-agent) |

please waiting for update

## Contribute

If you want to contribute to my project please don't hesitate to send a pull request. You can also join our users, by sending an email to [me](mailto:wulitouhaha@vip.qq.com), to ask questions and participate in discussions.


## Issue

if you hava some question or good idea,you can leave a message to me!


