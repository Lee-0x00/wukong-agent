# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: const foramt verify
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import sys,re
from splinter import Browser

#检查逐渐是否存活
def check_alive(host,timeout=1) :
	cmd = 'ping -c %d -w %d %s' % (1,timeout,host)
	p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	result = p.stdout.read()
	regex = re.findall('100% packet losss',result)
	if len(regex) == 0 :
		return True #´æ»î
	else:
		return False

#检查域名
def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', re.IGNORECASE)
    return True if domain_regex.match(domain) else False

#检查IP
def is_host(host):
    ip_regex = re.compile(r'(^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$)', re.IGNORECASE)
    return True if ip_regex.match(host) else False
    

#检查awvs域名格式
def awvs_target_check(test):
    result = ""
    browser = Browser("phantomjs")
    if is_domain(test):
        try:
            url = "https://"+str(test)
            browser.visit(url)
            browser.quit()
            return url
        except Exception as e:
            result = False

        try:
            url2 = "http://"+str(test)
            browser.visit(url2)
            browser.quit()
            return url2
        except Exception as e:
            result = False
    else:
        result = False
    return result
    # try:
    #     url = "https://"+str(test)
    #     url2 = "http://"+str(test)
    #     r = http_request_get(url)
    #     if int(r.status_code) == 200 :
    #         return url

    #     r2 = http_request_get(url2)
    #     if int(r.status_code) == 200 :
    #         return url2		
    # except:
    #     return False

