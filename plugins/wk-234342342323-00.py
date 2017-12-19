# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

import json, requests, csv, os, time
from core.settings import *
from utils.exploit import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#http.client


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


    def connect(self, token, resource, datas):
        headers = {'X-Cookie': 'token={0}'.format(token),'content-type': 'application/json'}
        data = json.dumps(datas)
        try:
            r = requests.post(url = str(nessus_url + resource) , data = data, headers = headers, verify= False)
        except:
            return False

        if r.status_code == 200:
            try:
                data = r.json()
            except:
                data = r.content
            return data       
        else:
            return False


    def exploit(self):
        #登陆
        resource = "/session"
        datas = {'username': nessus_name, 'password': nessus_pass}
        tokens = ""
        try:
            token = self.connect(tokens, resource, datas)["token"]
        except:
            return False

        #增加任务
        datas = {
            #"uuid": 'b9e01ede-c502-a064-cbca-e0f75d7743549709aaa0d800a65e',
            "uuid": "ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66",
            "settings" : {
                "name" : self.info["host"],
                "scanner_id": "1",
                "text_targets": self.info["host"],
                "enabled": False,
                "launch_now": True,
            }
        }
        resource = "/scans"
        result = self.connect(token, resource, datas)
        try:
            taskid = result["scan"]["id"]
        except:
            return False
        #遍历进程
        while True:
            time.sleep(30)
            headers = {'X-Cookie': 'token={0}'.format(token),'content-type': 'application/json'}
            try:
                data = requests.get(url = str(nessus_url + '/scans/'), params=None, headers = headers, verify=False)
                result = data.json()
            except:
                return False
            id_status = dict((b['id'], b['status']) for b in result['scans'])
            try:
                process = id_status[taskid]
            except:
                return False
            if str(process) == "completed" :
                break

        #获取报告ID
        resource = str('/scans/{0}/export'.format(taskid))
        datas = {"format" : "csv"}
        try:
            file_token = self.connect(token, resource, datas)["token"]
        except:
            return False
        
        #下载报告
        headers = {'X-Cookie': 'token={0}'.format(token),'content-type': 'application/json'}
        resource = str(nessus_url +'/scans/exports/{0}/download'.format(file_token))
        try:
            result = requests.get(url = resource, headers = headers, verify = False)
        except:
            return False
        csv_file = "{0}/{1}_nessus.csv".format(str(TMEP_REPORT_PATH),str(taskid))
        f = open(csv_file , 'wb')
        data = result.content
        f.write(data)
        f.close()

        #结果解析
        bug_list = {}
        with open(csv_file,"r",encoding="utf-8") as csvfile:
            csvReader = csv.reader(csvfile)
            for row in csvReader :
                bug = {}
                parameterStr = ','.join(row)   
                parameters = parameterStr.split(',')
                PID = parameters[0]
                CVE = parameters[1]  
                CVSS = parameters[2]  
                Risk = parameters[3]  
                Host = parameters[4]  
                Protocol = parameters[5]  
                Port = parameters[6]
                Name = parameters[7]  
                Synopsis = parameters[8]  
                Description = parameters[9]  
                Solution = parameters[10]  
                See_Also = parameters[11] 
                Plugin_Output = parameters[12] 

                bug_name = str(Name)
                bug_level = str(Risk)
                bug_summary = str(Synopsis)+"\r\n"+str(Description)
                bug_detail = "Bug Port : "+str(Port)+"\r\n"+"CVE : "+str(CVE)
                bug_repair = str(Solution)+"\r\n"+str(Plugin_Output)

                if str(Risk) in report_filter['nessus_white_list'] :
                    bug['bug_name'] = bug_name
                    bug['bug_desc'] = bug_summary
                    bug['bug_level'] = bug_level.lower()
                    bug['bug_result'] = bug_detail
                    bug['bug_repair'] = bug_repair
                    bug['bug_author'] = "bing"
                    bug["bug_type"] = other 

                    bug_list["status"] = True
                    bug_list["data"] = bug
                    self.result.append(bug_list)

        os.remove(csv_file)


# info = {
#     'scan_taskid': '3', 
#     'scan_protorl': 'http://', 
#     'scan_target': 'xxx.sdf.com', 
#     'scan_port': '80', 
#     'scan_cookie': 'sdf', 
#     'scan_proxy': 'sdf', 
#     'scan_user_agent': True, 
#     'plugin_name': 'nessus', 
#     'plugin_file': 'plugins/wk-174745431967-00.py', 
#     'model': 'brute', 
#     'fuzzing': {'user_pwd': '', 'brute_char': '80'}
# }
# t = wk(info)
# t.exploit()
# print(t.result)
