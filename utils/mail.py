# -*- coding:utf-8 -*- 
#!/usr/bin/env python3
#Description: wukong exploit 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

from core.settings import *
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


def add_img(src, imgid):
	'''
	添加图片函数；
		参数1： 图片路径； 参数2： 图片ID
	'''
	fp = open(src, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()
	# 指定图片文件的Content-ID, <img> 标签 src用到
	msgImage.add_header('Content-ID', imgid)

	return msgImage

def send_mail(host, pdf_path):
	'''
	发送邮件报告
	'''
	#主题邮件内容
	contents = """
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>未来安全局</title>
		    <style>
		        .smart-green {
		            margin-left: auto;
		            margin-right: auto;
		            max-width: 500px;
		            background: #F8F8F8;
		            padding: 30px 30px 20px 30px;
		            font: 12px Arial, Helvetica, sans-serif;
		            color: #666;
		            border-radius: 5px;
		            -webkit-border-radius: 5px;
		            -moz-border-radius: 5px;
		        }

		        .smart-green h1 {
		            font: 24px "Trebuchet MS", Arial, Helvetica, sans-serif;
		            padding: 20px 0px 20px 40px;
		            display: block;
		            margin: -30px -30px 10px -30px;
		            color: #FFF;
		            background: #9DC45F;
		            text-shadow: 1px 1px 1px #949494;
		            border-radius: 5px 5px 0px 0px;
		            -webkit-border-radius: 5px 5px 0px 0px;
		            -moz-border-radius: 5px 5px 0px 0px;
		            border-bottom: 1px solid #89AF4C;
		        }

		        .smart-green h1 > span {
		            display: block;
		            font-size: 11px;
		            color: #FFF;
		        }

		        .smart-green label {
		            display: block;
		            margin: 0px 0px 5px;
		        }


		        .smart-green input[type="text"], .smart-green input[type="email"], .smart-green textarea, .smart-green select {
		            color: #555;
		            height: 30px;
		            line-height: 15px;
		            width: 100%;
		            padding: 0px 0px 0px 10px;
		            margin-top: 2px;
		            border: 1px solid #E5E5E5;
		            background: #FBFBFB;
		            outline: 0;
		            -webkit-box-shadow: inset 1px 1px 2px rgba(238, 238, 238, 0.2);
		            box-shadow: inset 1px 1px 2px rgba(238, 238, 238, 0.2);
		            font: normal 14px/14px Arial, Helvetica, sans-serif;
		        }

		        .smart-green textarea {
		            height: 200px;
		            padding-top: 10px;
		            display: block;
		            font-size: 11px;
		        }


		        .smart-green .button {
		            background-color: #9DC45F;
		            border-radius: 5px;
		            -webkit-border-radius: 5px;
		            -moz-border-border-radius: 5px;
		            border: none;
		            padding: 10px 25px 10px 25px;
		            color: #FFF;
		            text-shadow: 1px 1px 1px #949494;
		        }

		        .smart-green .button:hover {
		            background-color: #80A24A;
		        }

		    </style>
		</head>
		<body>
		<form action="/form/" method="post" class="smart-green">
		    <h1>未来安全探测者
		        <span>安全无小事</span>
		    </h1>

		    <p><label><span style="font-size: 13px;">亲爱的小伙伴 !!!
		    </br></br>
		    &nbsp;&nbsp;&nbsp;&nbsp;见信好！通过未来安全探测者的安全分析，发现您的资产信息存在弱点; 请查阅附件进行修复 , thank you for readding!</span></label></p>

		</form>

		</body>
		</html>
	"""
	msgtext = MIMEText(contents, _subtype = 'html', _charset = 'UTF-8')


	# 创建MIMEMultipart对象, 附加MIMEImage的内容
	msg = MIMEMultipart()

	# MIMEMultipart对象附加MIMEText内容[html]
	msg.attach(msgtext)

	# 图片内容： MIMEMultipart对象附加MIMEImage内容[图片]
	# msg.attach(add_img('img/weekly.jpg', 'weekly'))

	# 附件：创建一个MIMEApplication对象，附加week_report.pdf 
	pdfpart = MIMEApplication(open('%s' % pdf_path, 'rb').read())
	pdfpart.add_header('Content-Disposition', 'attachment', filename='%s业务安全质量报告.pdf' % host )
	msg.attach(pdfpart)


	SUBJECT = "%s业务安全质量报告----未来安全局" % host 
	msg["SUBJECT"] = SUBJECT
	msg["From"] = EMAIL_HOST_USER
	msg["To"] = EMAIL_TO

	try:
		server = smtplib.SMTP()
		server.connect(EMAIL_HOST)
		server.login(EMAIL_HOST_USER , EMAIL_HOST_PASSWORD)
		server.sendmail(EMAIL_HOST_USER, EMAIL_TO, msg.as_string())
		server.quit()
		return True 
	except Exception as e:
		return False


