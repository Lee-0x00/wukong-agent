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


# info = {
#     'scan_taskid': '3', 
#     'scan_protorl': 'http://', 
#     'scan_target': 'xxx.sdf.com', 
#     'scan_port': '80', 
#     'scan_cookie': 'sdf', 
#     'scan_proxy': 'sdf', 
#     'scan_user_agent': True, 
#     'plugin_name': '端口扫描', 
#     'plugin_file': 'plugins/wk-174745431967-00.py', 
#     'model': 'brute', 
#     'fuzzing': {'user_pwd': '', 'brute_char': '80'}
# }
# t = wk(info)
# # t.start(443)
# t.exploit()
# print(t.result)
