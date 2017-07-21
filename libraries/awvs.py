#!/user/bin python
# -*- coding:utf-8 -*- 
# Author:Bing
# Contact:amazing_bing@outlook.com
# DateTime: 2017-01-17 19:06:06
# Description:  coding 

import sys
sys.path.append("..")

import httplib,json,urllib2
from datetime import datetime
from time import gmtime, strftime
from xml.dom import minidom
import random,time,os,sys
import zipfile,cgi  

from core.settings import talscan_config,redis_task
from common.wukong_TypeCheck import *

class Work(object):
    def __init__(self, scan_id = "", scan_target = "", scan_type = "" , scan_args = "", back_fn = None):
        self.api_url = talscan_config["awvs_url"]
        self.api_header = talscan_config["awvs_header"]
        self.filter = talscan_config["report_filters"]
        self.api_port = talscan_config["awvs_port"]
        self.report_save_dir = talscan_config["report_save_dir"]

        self.scan_id = scan_id
        self.target = scan_target
        self.scan_type = scan_type
        self.args = scan_args
        self.back_fn = back_fn
        self.result = {}

    def parse_xml(self,file_name):
        bug_list = []
        root = minidom.parse(file_name).documentElement
        ReportItem_list =  root.getElementsByTagName('ReportItem')

        if ReportItem_list:
            for node in ReportItem_list:
                color = node.getAttribute("color")
                name = node.getElementsByTagName("Name")[0].firstChild.data.encode('utf-8')

                try:
                    if color in self.filter['awvs_white_list'] and name not in self.filter['bug_black_list']:
                        temp = {}
                        temp['bug_name'] = '{0}'.format(name)
                        temp['color'] = '{0}'.format(color.encode('utf-8'))
                        temp['bug_summary'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Details")[0].firstChild.data.encode('utf-8')))
                        temp['bug_level'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Severity")[0].firstChild.data.encode('utf-8')))

                        affect = '{0}'.format(node.getElementsByTagName("Affects")[0].firstChild.data.encode('utf-8'))

                        try:
                            request = '{0}'.format(cgi.escape(node.getElementsByTagName("Request")[0].firstChild.data.encode('utf-8')))
                        except:
                            request = ""

                        try:
                            response = '{0}'.format(cgi.escape(node.getElementsByTagName("Response")[0].firstChild.data.encode('utf-8')))
                        except:
                            response = ""

                        temp['bug_detail'] = "漏洞链接 : " + affect + "  Detail : " + request + response
                        temp['bug_repair'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Recommendation")[0].firstChild.data.encode('utf-8')))

                        bug_list.append(temp)
                except Exception, e:
                    pass

            result = {"status":1,"data":bug_list}
            return result
        else:
            result = {"status":0}
            return result


    def download(self,path_file,data):
        try:
            with open("{0}".format(path_file), "wb") as code:     
                code.write(data)
                code.close()
            return {"status":1,"data":path_file}
        except:
            return {"status":0}

    def unzip_dir(self,unzipfilename, savexmlfile):
        result = ""
        try:
            srcZip = zipfile.ZipFile(unzipfilename, "r")
            for eachfile in srcZip.namelist():
                if eachfile.endswith(".xml",3):
                    fd=open(savexmlfile, "wb")
                    result = savexmlfile
                    fd.write(srcZip.read(eachfile))
                    fd.close()
            srcZip.close()
            return {"status":1,"data":result}
        except:
          return {"status":0}


    def awvs_add_task(self,loginSeq=""):
        target = awvs_target_check(self.target)
        if int(datetime.now().minute) == 58 or int(datetime.now().minute) == 59 :
            days = (datetime.now().hour+1,0)
        else:
            days = (datetime.now().hour, datetime.now().minute+2)

        if target == False :
            return { "status" : 2 , "data" : "AWVS >>>> 格式错误" }
        try:
            ACUDATA = {"scanType":"scan",
                       "targetList":"",
                       "target":["%s" % target],
                       "recurse":"-1",
                       "date":strftime("%m/%d/%Y", gmtime()),
                       "dayOfWeek":"1",
                       "dayOfMonth":"1",
                       "time": "%s:%s" % days,
                       "deleteAfterCompletion":"False",
                       "params":{
                                "profile":"Default",
                                 "loginSeq":str(loginSeq),
                                 "settings":"Default",
                                 "scanningmode":"heuristic",
                                 "excludedhours":"<none>",
                                 "savetodatabase":"False",
                                 "savelogs":"False",
                                 "ExportXML":"export.xml",
                                 "emailaddress":""
                                }
                       }
        except:
            return {"status":0}

        try:
            conn = httplib.HTTPConnection(self.api_url, self.api_port)
            conn.request("POST", "/api/addScan", json.dumps(ACUDATA) , self.api_header)
            resp = conn.getresponse()
            content = resp.read()
        except:
            return {"status":2}

        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            taskid = result["data"][0].encode("gbk")
            return {"status":1,"data":taskid}
        else:
            return {"status":0}


    def awvs_process_status(self,taskid):
        try:
            conn_p = httplib.HTTPConnection(self.api_url, self.api_port)
            data = json.dumps({'id': str(taskid)})
            conn_p.request("POST", "/api/getScanHistory", data, self.api_header)
            resp2 = conn_p.getresponse()
            awvs_process_content = resp2.read()

            conn = httplib.HTTPConnection(self.api_url, self.api_port)
            conn.request("GET", "/api/listScans", headers=self.api_header)
            resp = conn.getresponse()
            awvs_list_content = resp.read()
        except:
            return {"status":2}

        awvs_process_result = json.loads(awvs_process_content)
        awvs_list_result = json.loads(awvs_list_content)
        status = awvs_process_result["result"].encode("gbk")
        list_status = awvs_list_result["result"].encode("gbk")
        if status == "OK" and len(awvs_process_result["data"]) > 0 :
            process = awvs_process_result["data"][-1]["msg"].encode("gbk")
            if "Scan finished" in process:
                return {"status":1,"data":100}

            if list_status == "OK":
                for i in awvs_list_result["data"]["scans"] :
                    task_id = i["id"].encode("gbk")
                    if str(task_id) == str(taskid):
                        task_process =  i["progress"]
                return {"status":1,"data":task_process}
        else:
            return {"status":0}


    def awvs_report_task(self,taskid,awvsid):
        save_dir = self.report_save_dir
        try:
            conn = httplib.HTTPConnection(self.api_url, self.api_port)
            data = json.dumps({"id":str(awvsid)})
            conn.request("POST", "/api/getScanResults", data , self.api_header)
            resp = conn.getresponse()
            content = resp.read()
        except:
            return {"status":2}

        result = json.loads(content)
        status = result["result"].encode("gbk")
        try:
            result_len = len(result["data"][0])
        except:
            result_len = 2

        if status == "OK" and result_len == 3:
            try:
                report_id = result["data"][0]["id"].encode("gbk")
                conn.request("GET", "/api/download/{0}:{1}".format(awvsid, report_id), headers=self.api_header)
                resp = conn.getresponse()
                download_contents = resp.read()

                #保持报告文件
                zipfilename = "{0}{1}_awvs.zip".format(str(save_dir),str(taskid))
                xmlfilename = "{0}{1}_awvs.xml".format(str(save_dir),str(taskid))

                download_file = self.download(path_file=zipfilename,data=download_contents)
                if download_file['status'] == 1:
                    xml_filename = self.unzip_dir(unzipfilename=zipfilename,savexmlfile=xmlfilename)
                    #print xml_filename
                    if xml_filename["status"] == 1:
                        os.remove(zipfilename)
                        xml_data = self.parse_xml(xml_filename["data"])
                        if xml_data['status'] == 1:
                            os.remove(xmlfilename)
                            return {"status":1,"data":xml_data["data"]}
                        else:
                            return {"status": 2}
                else:
                    return {"status":2}
            except:
                return {"status":0}
        else:
            return {"status":0}

    def awvs_list_loginseq(self):
        cookie_dir = loginseq_dir
        content = []
        for parent,dirnames,filenames in os.walk(cookie_dir):
            for filename in filenames:
                content.append(filename)
        result = {"status":1,"data":content}
        return result


    def run(self):
        result = self.awvs_add_task()
        status = result["status"]
        if status == 1 :
            awvs_id = int(result["data"])  
            while True:
                time.sleep(5)
                awvs_process = self.awvs_process_status(awvs_id)
                awvs_status = awvs_process["status"]
                if awvs_status == 1 :
                    awvs_process_data = awvs_process["data"]
                    if awvs_process_data == 100 :
                        break

            time.sleep(50)       #推迟50秒，获取报告;awvs任务进程到100有部分延迟结束时间
            awvs_report = self.awvs_report_task(self.scan_id,awvs_id)  
            awvs_report_status = awvs_report["status"]
            if awvs_report_status == 1 :
                awvs_report_data = awvs_report["data"]
                data = []
                for line in awvs_report_data : 
                    task_result = {
                        "scan_id": self.scan_id , 
                        "model": "awvs" ,
                        "bug_author" : "bing" ,
                        "bug_name" : line["bug_name"] ,
                        "bug_level" : line["bug_level"] ,
                        "bug_summary" : line["bug_summary"]  ,
                        "bug_detail" : line["bug_detail"]  ,
                        "bug_repair" : line["bug_repair"] 
                    }

                    redis_task.sadd("awvs_result",task_result)
                    print task_result

                #任务最终结束
                final_result = { "status" : 1 , "scan_id": self.scan_id , "model": "awvs" }

                redis_task.sadd("awvs_result",final_result)
                print final_result

            else:
                #任务最终结束
                final_result = { "status" : 1 , "scan_id": self.scan_id , "model": "awvs" }

                redis_task.sadd("awvs_result",final_result)
                print final_result

        elif status == 2 :
            awvs_error = result["data"]
            final_result = { "status" : 2 , "data" : awvs_error , "scan_id": self.scan_id , "model": "awvs" }

            redis_task.sadd("awvs_result",final_result)
            print final_result



# t = Work(scan_id = "test-233", scan_target = "100.xueersi.com" )
# t.run()


