# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: const foramt verify
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import re,os,subprocess
from subprocess import Popen, PIPE
from platform import system
from splinter import Browser

def is_Alive(ip):
    if system()=='Linux':
        p=Popen(['ping','-c 2',ip],stdout=PIPE)
        m = re.search('ttl', p.stdout.read())
        if m:
            return ip
        else:
            return False
    if system()=='Windows':
        p=Popen('ping %s -n 2'%ip,stdout=PIPE)
        m = re.search('TTL', p.stdout.read())
        if m:
            return ip
        else:
            return False


def check_Alive(host,timeout=1) :
    cmd = 'ping -c %d -w %d %s' % (1,timeout,host)
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    result = p.stdout.read()
    regex = re.findall('100% packet loss',result)
    if len(regex) == 0 :
        return True 
    else:
        return False


def is_Domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', re.IGNORECASE)
    return True if domain_regex.match(domain) else False


def is_Host(host):
    ip_regex = re.compile(r'(^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$)', re.IGNORECASE)
    return True if ip_regex.match(host) else False


def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("test")
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



def get_DocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print err

def awvs_target_check(test):
    result = ""
    browser = Browser("phantomjs")
   
    try:
        url = "https://"+str(test)
        browser.visit(url)
        browser.quit()
        return url
    except:
        result = False

    try:
        url2 = "http://"+str(test)
        browser.visit(url2)
        browser.quit()
        return url2
    except:
        result = False

    return result
