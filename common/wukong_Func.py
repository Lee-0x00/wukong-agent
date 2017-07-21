# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: usually function(public)
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys
sys.path.append("..")

import re,smtplib,os
from email.mime.text import MIMEText
import dns.resolver,requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from core.settings import talscan_config,POC_PATH,dict_script_path

#**************************************************request 请求配置********************************************************************

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

def random_useragent(condition=False):
    if condition:
        return random.choice(USER_AGENTS)
    else:
        return USER_AGENTS[0]

def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
    else:
        return '8.8.8.8'

headers = {
    'User-Agent': random_useragent(talscan_config["allow_random_useragent"]),
    'X_FORWARDED_FOR': random_x_forwarded_for(talscan_config["allow_random_x_forward"]),
    'Referer' : 'http://www.google.com',
    'Cookie': talscan_config["custom_cookie"],
}


if talscan_config["allow_http_session"]:
    requests = requests.Session()

#get请求
def http_request_get(url, body_content_workflow=True, allow_redirects= talscan_config["allow_redirects"], custom_cookie= talscan_config["custom_cookie"]):
    try:
        if talscan_config["custom_cookie"]:
            headers['Cookie'] = talscan_config["custom_cookie"]
        result =  requests.get(url=url, stream= body_content_workflow, headers= headers, timeout= talscan_config["timeout"], proxies= talscan_config["proxies"],allow_redirects = allow_redirects,verify = talscan_config["allow_ssl_verify"])
        return result
    except Exception, e:
        return ""

#post请求
def http_request_post(url, payload, body_content_workflow=True, allow_redirects= talscan_config["allow_redirects"], custom_cookie= talscan_config["custom_cookie"]):
    try:
        if talscan_config["custom_cookie"]:
            headers['Cookie']= talscan_config["custom_cookie"]
        result = requests.post(url=url, data=payload, stream= body_content_workflow, headers= headers, timeout= talscan_config["timeout"], proxies= talscan_config["proxies"],allow_redirects = allow_redirects,verify = talscan_config["allow_ssl_verify"])
        return result
    except Exception, e:
        return ""


#**************************************************poc or dict 本地查找********************************************************************
def get_web_poc( module , scan_type): 
	suggestions = []
	files = os.listdir(POC_PATH)
	pattern = '^(' + module + '_).*?' + scan_type + '.*?\.py$'  
	#pattern = '.*?'+user_input+'.*?\.py$'
	regex = re.compile(pattern) 
	for item in files:
		match = regex.search(item) 
		if match and item != '__init__.py':
			suggestions.append((len(match.group()), match.start(), POC_PATH+'/'+item))
	return [x for _, _, x in sorted(suggestions)]


def get_dict(poc_name):
    pattern = 'brute_(.*)_.*?\.py$' 
    poc_dict_filename = re.findall(pattern,poc_name)[0]
    subprefix = []
    #也可以改成 post：poc_dict_filename 到api 获取不同类型的数值
    files = os.listdir(dict_script_path)
    for item in files :
        if poc_dict_filename in item and poc_dict_filename == "subdomain" :
            filename_path = dict_script_path + str(item)
            with open(filename_path,"r") as server:
                for finger in server.readlines():
                    subprefix.append(finger.strip())
        if poc_dict_filename in item and poc_dict_filename == "redis" :
            filename_path = dict_script_path + str(item)
            with open(filename_path,"r") as server:
                for finger in server.readlines():
                    subprefix.append(finger.strip())

        if poc_dict_filename in item and poc_dict_filename == "qqmail" :
            filename_path = dict_script_path + str(item)
            with open(filename_path,"r") as server:
                for finger in server.readlines():
                    test = finger.strip().split(":")
                    subprefix.append((test[0],test[1]))

        # if poc_dict_filename in item and poc_dict_filename == "subdomain" :
        #     filename_path = dict_script_path + str(item)
        #     with open(filename_path,"r") as server:
        #         for finger in server.readlines():
        #             subprefix.append(finger.strip())
    return subprefix

#print get_dict("brute_qqmail_12532324.py")


#************************************************** 邮箱功能 ********************************************************************

def mail_notify(title = "Talscan Notice !!! " , content = " " , mailto_list = ['test@100tal.com']):
    me="talscan" + "<" + mail_user + "@" + mail_postfix +">"
    contents = """
        <html>
        <head>
        <style>
            body { 
                font-family: Arial, Helvetica, sans-serif; font-size : 12px ;  
            }
        </style>
        </head>
        <body>  
        <div style="margin:auto;margin_top:50px;">
            <p>
                <h1>欢迎来到好未来扫描平台！！!</h1>
                <br><br>%s</span>请到数据库进行收账。。。  过期不候!
            </p>
        </div>
        </body>  
        </html>  
    """ % content

    msg = MIMEText(contents,_subtype='html',_charset='UTF-8')
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

#mail_notify(taskid = "test" , title = "Talscan Notice !!! " , content = "Welcome to Talscan platfrom ... " , mailto_list = ['security@100tal.com'])

