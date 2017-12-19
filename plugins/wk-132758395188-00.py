# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

import http.client,json,requests,zipfile,cgi,time,os,random
from datetime import datetime
from time import gmtime, strftime
from xml.dom import minidom 
from core.settings import *
from utils.exploit import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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


    def parse_xml(self,file_name):
        #解析xml数据
        root = minidom.parse(file_name).documentElement
        ReportItem_list =  root.getElementsByTagName('ReportItem')

        if ReportItem_list:
            for node in ReportItem_list:
                color = node.getAttribute("color")
                name = node.getElementsByTagName("Name")[0].firstChild.data
                try:
                    if color in report_filter['awvs_white_list'] and name not in report_filter['bug_black_list']:
                        temp = {}
                        temp['bug_name'] = '{0}'.format(name)
                        temp["bug_author"] = "bing" 

                        temp['bug_ref'] = ''
                        temp['bug_desc'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Details")[0].firstChild.data))
                        temp['bug_level'] = '{0}'.format(node.getElementsByTagName("Severity")[0].firstChild.data.lower())

                        affect = '{0}'.format(node.getElementsByTagName("Affects")[0].firstChild.data)

                        try:
                            request = '{0}'.format(cgi.escape(node.getElementsByTagName("Request")[0].firstChild.data))
                        except:
                            request = ""

                        try:
                            response = '{0}'.format(cgi.escape(node.getElementsByTagName("Response")[0].firstChild.data))
                        except:
                            response = ""

                        test = "Vulnerability link : " + affect + "\n Detail : \n" + request + "\n"+ response
                        txt = test.replace('\n','<br/>')
                        temp['bug_result'] = [txt]
                        temp['bug_repair'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Recommendation")[0].firstChild.data))
                        temp["bug_type"] = "awvs" 
                        bug_list = {}
                        bug_list["status"] = True
                        bug_list["data"] = temp
                        self.result.append(bug_list)
                except:
                    pass

            return True
        else:
            return False


    def connect(self, method, resource, data = None):
        try:
            conn = http.client.HTTPConnection(awvs_url, awvs_port)
            conn.request(method, resource, json.dumps(data) , awvs_header)
            resp = conn.getresponse()
            content = resp.read()
            return content
        except Exception as e:
            return False


    def exploit(self):
        #增加任务
        target = self.info["protorl"] + self.info["host"] + ":" + str(self.info["port"])
        now_date = time.time()
        start_date = now_date + 60*3    
        days = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(start_date)).split(" ")[0]
        hour = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(start_date)).split(" ")[1].split(":")[0]
        minutes = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(start_date)).split(" ")[1].split(":")[1]
        ACUDATA = {
            "scanType":"scan",
            "targetList":"",
            "target":["%s" % target],
            "recurse":"-1",
            "date": days,
            "dayOfWeek":"1",
            "dayOfMonth":"1",
            "time": "%s:%s" % (hour,minutes),
            "deleteAfterCompletion":"False",
            "params":{
                "profile":"Default",
                "loginSeq":str(self.info["cookie"]),
                "settings":"Default",
                "scanningmode":"extensive",
                "excludedhours":"<none>",
                "savetodatabase":"False",
                "savelogs":"False",
                "ExportXML":"export.xml",
                "emailaddress":""
                }
        }

        data = self.connect("POST", "/api/addScan", ACUDATA)
        if not data :
            return True
        result = json.loads(data)
        status = result["result"]
        if status == "OK":
            taskid = result["data"][0]
            ACUDATA = {'id': str(taskid)}
            while True:
                time.sleep(30)
                #获取扫描进程
                awvs_process_data = self.connect("POST", "/api/getScanHistory", ACUDATA)
                if not awvs_process_data :
                    return True
                awvs_process_result = json.loads(awvs_process_data)
                awvs_process_status = awvs_process_result["result"]
                if awvs_process_status == "FAIL" :
                    return True
                #判断是否完成
                if awvs_process_status == "OK" and len(awvs_process_result["data"]) > 0 :
                    process = awvs_process_result["data"][-1]["msg"]
                    if "Scan finished" in process:
                        break
                    else:
                        continue
            #获取报告
            ACUDATA = {"id":str(taskid)}
            data = self.connect("POST", "/api/getScanResults", ACUDATA)
            if not data :
                return True
            result = json.loads(data)
            status = result["result"]
            result_len = len(result["data"][0])

            if status == "OK" and result_len == 3:
                report_id = result["data"][0]["id"] 
                data = self.connect("GET", "/api/download/{0}:{1}".format(taskid, report_id))
                if not data :
                    return True
                #{'result': 'OK', 'data': [{'id': '334508baa98ba7a245b95944d5c5b2f1', 'date': '周二 12 12月 2017, 11:49:57', 'size': '16.44 KB'}]}
                zipfilename = "{0}/{1}_awvs.zip".format(str(TMEP_REPORT_PATH),str(random.randint(1,200)))
                xmlfilename = "{0}/{1}_awvs.xml".format(str(TMEP_REPORT_PATH),str(random.randint(1,200)))
                #download report and unzip file and format file
                try:
                    with open("{0}".format(zipfilename), "wb") as code:     
                        code.write(data)
                        code.close()
                except:
                    return True
                xml_filename = ""
                try:
                    srcZip = zipfile.ZipFile(zipfilename, "r")
                    for eachfile in srcZip.namelist():
                        if eachfile.endswith(".xml",3):
                            fd=open(xmlfilename, "wb")
                            xml_filename = xmlfilename
                            fd.write(srcZip.read(eachfile))
                            fd.close()
                    srcZip.close()
                except:
                    return True
                os.remove(zipfilename)
                xml_data = self.parse_xml(xml_filename)
                if xml_data:
                    os.remove(xmlfilename)
                return True
        else:
            return True 


# info = {
#     'scan_taskid': '3', 
#     'scan_protorl': 'http://', 
#     'scan_target': 'xxx.sdf.com', 
#     'scan_port': '80', 
#     'scan_cookie': 'sdf', 
#     'scan_proxy': 'sdf', 
#     'scan_user_agent': True, 
#     'plugin_name': 'awvs', 
#     'plugin_file': 'plugins/wk-test-00.py', 
#     'model': 'brute', 
#     'fuzzing': {'user_pwd': '', 'brute_char': '80'}
# }
# t = wk(info)
# # t.start(443)
# t.exploit()
# print(t.result)
