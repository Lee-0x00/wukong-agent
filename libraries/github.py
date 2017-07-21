#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("..")
import time
import urllib
import requests
import datetime
import random
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding("utf-8")

from core.settings import redis_task

session = requests.session()
header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'HTTPS':'1',
            'Referer':'https://github.com/',
            'Origin':'https://github.com',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Accept-Encoding':'gzip, deflate, br',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }

# get login token
csrfToken = pq(session.get('https://github.com/login', headers=header).text)('input[name="authenticity_token"]').val()
loginData = {'login':'fennudehexie', 'password':'youyudehexie123', 'authenticity_token': csrfToken, 'utf8':'✓'} 
res = session.post('https://github.com/session', data=loginData, headers=header)

def submitMsg(keyword, projectTitle, projectUrl, fileTitle, fileUrl, code):
    data = {'keyword': keyword, 'projectTitle': projectTitle, 'projectUrl': projectUrl, 'fileTitle':fileTitle, 'fileUrl':fileUrl, 'code': code}

def query(keyword):
    rs = []
    page = 1
    keywordTmp = urllib.quote(keyword)
    keywordTmp = keywordTmp.replace("%20", "+")
    while True:
        time.sleep(random.randint(1, 5))
        url = "https://github.com/search?p=%d&q=%s&ref=searchresults&type=Code&utf8=%s&s=indexed&o=desc" % (page, keywordTmp, "%E2%9C%93")

        print url
        page = page+1
        code = session.get(url, headers=header).text
        soup = BeautifulSoup(code, "lxml")
        tmpList = soup.find_all(class_="code-list-item")

        noNext = code.find("<span class=\"next_page disabled\">Next</span>") > -1 or code.find("Next") == -1
	print noNext
        if noNext:
            print "####"+url

        for item in tmpList:
            site = "https://www.github.com"
            addr = item.find('div').find_all('a')
            projectUrl = site + addr[0].get('href')
            projectTitle = addr[0].text
            fileUrl = site + addr[1].get('href')
            fileTitle = addr[1].text
            code = str(item.find('table'))
            submitMsg(keyword, projectTitle, projectUrl, fileTitle, fileUrl, code)
        rs = rs + tmpList

        if noNext:
            break
    return rs

def run(scan_id = "" , scan_target = "" , scan_args = []) :
    all = []
    target = str(".".join(scan_target.split(".")[1:]))

    keywords = [{"word":"{0}+smtp".format(target)},{"word":"{0}+password".format(target)},{"word":"{0}+pwd".format(target)}]
    if len(scan_args) > 0 :
        for key in scan_args :
            keywords.append({"word":"{0}+{1}".format(target,key)})

    for keyword in keywords:
        print keyword['word']
        rs = query(keyword['word'])
        if len(rs) > 0:
            all = all + rs
    for item in all:
        bug_detail = str(item).replace("href=\"", "target=\"_blank\" href=\"https://www.github.com")
        task_result = {
                "scan_id": scan_id , 
                "model": "github" ,
                "bug_author" : "bing" ,
                "bug_detail" : bug_detail
            }
        redis_task.sadd("github_result",task_result)
        print task_result

    final_result = { "status" : 1 , "scan_id": scan_id , "model": "github" }
    redis_task.sadd("github_result",final_result)
    print final_result

