# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

from core.settings import *
from utils.mail import send_mail
import requests, time, re
from reportlab.pdfgen.canvas import Canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont 
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))  
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle


def custom_upload_result(taskid, host, result):
	'''
	自定义上传结果数据
	api & local backup
	'''
	bug_name = str(result["bug_name"])
	bug_type = str(result["bug_type"])
	bug_level = str(result["bug_level"].lower())
	bug_desc = str(result["bug_desc"])
	bug_result = result["bug_result"].__str__()
	bug_repair = str(result["bug_repair"])

	try:
		'''
		node_ip;time;process;content
		'''
		#待编写,先验证数据格式，在上传
		requests.post(url = "12743", data = "", cookies = "")
		return True
	except:
		pass

	# # 登陆post
	# s = requests.session()
	# try:
	# 	s.post(url = login_url,data = user_pwd)
	# except:
	# 	pass

	# # 结果数据
	# datas = {
	# 	"obj" : "add",
	# 	"taskid" : taskid,			
	# 	"domain" : host,
	# 	"name" : bug_name ,
	# 	"types" : bug_type ,
	# 	"level" : bug_level ,
	# 	"summary" : bug_desc ,
	# 	"result" : bug_result,
	# 	"repair" : bug_repair
	# }

	# # 上传结果
	# try:
	# 	s.post(url = result_url, data = datas)
	# 	#print(上传成功的日志)
	# except:
	# 	#print(上传失败的日志)
	# 	pass


	#本地保存结果
	result_text = "{0}/{1}_report.txt".format(TMEP_REPORT_PATH, taskid)
	txt = open(result_text,"a+")

	html_title = ""
	html_port = ""
	html_bug = ""
	html_finish = ""

	try:
		if bug_name == "start" :
			# pdf第一次的title数据
			curr_date = time.strftime("%Y-%m-%d", time.localtime())
			html_title = '''
			    <para autoLeading="off" fontSize=12>
			    <font face="msyh" fontSize=20>%s扫描报告</font>
			    <br/>
			    <br/>
			    <font face="msyh" fontSize=16>%s</font>
			    <br/>
			    <br/>
			    <br/>
			    <br/>
			    </para>
			    <para fontSize=12>
			''' % (host, curr_date)
		elif bug_name == "端口扫描" :
			# 端口数据
			port_info = '<font face="msyh">%s</font><br/>' % ( bug_result )
			html_port = '''
			    <font face="msyh">开放端口：</font><br/>
			    <br/>
			    %s
			    <br/>
			    <br/>
			    <br/>
			    ----------------------------------------------------------------------------------------------------
			''' % port_info
		elif bug_name == "finish" :
			# 结束字符
			html_finish = '</para>'
		else :
			# 漏洞数据
			level_text = ""
			if bug_level == "high" :
				level_text = '<font face="msyh" >漏洞等级：</font><font face="msyh" color=red> %s</font><br/>' %  bug_level
			elif bug_level == "medium" :
				level_text = '<font face="msyh" >漏洞等级：</font><font face="msyh" color=orange> %s</font><br/>' %  bug_level
			elif bug_level == "low" :
				level_text = '<font face="msyh" >漏洞等级：</font><font face="msyh" color=green> %s</font><br/>' %  bug_level
			else:
				level_text = '<font face="msyh" >漏洞等级：</font><font face="msyh" color=green> %s</font><br/>' %  bug_level

			html_bug = '''
			    <br/>
			    <font face="msyh" >漏洞名称： %s</font><br/>
			    <br/>
			    %s
			    <br/>
			    <font face="msyh" >漏洞简介：</font><br/>
			    <br/>
			    <font face="msyh" >%s</font><br/>
			    <br/>
			    <font face="msyh" >漏洞详情： </font><br/>
			    <br/>
			    <font face="msyh" >%s</font><br/>
			    <br/>
			    <font face="msyh" >修复建议：</font><br/>
			    <br/>
			    <font face="msyh" >%s</font><br/>
			    <br/>
			    <br/>
			    <br/>
			    ----------------------------------------------------------------------------------------------------
			''' % ( bug_name , level_text , bug_desc , bug_result , bug_repair )

		html = html_title + html_port + html_bug + html_finish
		txt.write( html )
		txt.write("\n")
		txt.close()
	except:
		txt.close()

	return True


def custom_upload_log(taskid, process, content):
	'''
	自定义上传日志数据
	api & local backup
	'''
	try:
		'''
		node_ip;time;process;content
		'''
		#待编写,先验证数据格式，在上传
		requests.post(url = "12743", data = "", cookies = "")
		return True
	except:
		pass

	# # 登陆post
	# s = requests.session()
	# try:
	# 	s.post(url = login_url, data = user_pwd)
	# except:
	# 	pass

	# # 日志数据
	# datas = {
	# 	"obj" : "log",
	# 	"taskid" : taskid,
	# 	"process" : process,
	# 	"log" : error_info
	# }
	
	# # 上传日志
	# try:
	# 	s.post(url = log_url, data = datas)
	# 	print("日志上传成功")
	# except:
	# 	print("日志上传失败")
	# 	pass

	result_text = "{0}/{1}_log.txt".format(TMEP_REPORT_PATH, taskid)
	result = open(result_text,"a+")
	html = str( (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) ) + "; "+ str(process) + "; "+ str(content)
	result.write( html )
	result.write("\n")
	result.close()
	return True



def custom_divide_domain(url):
	'''
	分割url
	'''
	host_protocol = "" 
	host_name = "" 
	host_port = "" 
	host_path = "" 

	reg_p = re.compile(r'http\:\/\/|https\:\/\/', re.IGNORECASE)
	reg_h = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', re.IGNORECASE)
	reg_d = re.compile(r'((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}', re.IGNORECASE)
	reg_port = re.compile(r'\:[0-9]{1,5}' , re.IGNORECASE)

	search_http = reg_p.search(url) 
	search_h = reg_h.search(url)
	search_d = reg_d.search(url)
	search_port = reg_port.search(url)
	if search_http :
		host_protocol = search_http.group()

	if search_h :
		host_name = search_h.group()

	if not search_h :
		if search_d :
			host_name = search_d.group()

	if search_port :
		host_port = search_port.group().split(":")[1]

	return (host_protocol , host_name , host_port) 


def make_pdf_report(host, taskid):
	'''
	生成pdf报告
	'''
	data = []
	result_text = "{0}/{1}_report.txt".format(TMEP_REPORT_PATH, taskid)
	result = open(result_text,"r")
	for line in result.readlines():
		data.append(line.strip()) 
	html = ''.join(data)

	if "漏洞名称" in html:
		pdfname = '{0}/{1}.pdf'.format(TMEP_REPORT_PATH,taskid)
		story=[]
		stylesheet=getSampleStyleSheet()
		normalStyle = stylesheet['Normal']
		story.append(Paragraph(html,normalStyle)) 
		doc = SimpleDocTemplate(pdfname)
		doc.build(story)
		send_mail(host, pdfname)
		return True
	else:
		return False


def formatSize(bytes):
	'''
	计算文件大小
	'''
	try:
		bytes = float(bytes)
		kb = bytes / 1024
	except:
		return "Error"

	if kb >= 1024:
		M = kb / 1024
		if M >= 1024:
			G = M / 1024
			return "%fG" % (G)
		else:
			return "%fM" % (M)
	else:
		return "%fkb" % (kb)


def getDocSize(path):
	'''
	获取文件大小
	'''
	try:
		size = os.path.getsize(path)
		return formatSize(size)
	except Exception as err:
		print(err)
