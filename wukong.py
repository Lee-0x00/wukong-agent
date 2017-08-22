# -*- coding:utf-8 -*- 
#!/user/bin python
#Description: celery task 
#Author:      Bing
#Email:       amzing_bing@outlook.com
#DateTime:    2017-05-10 23:08:39

import time,subprocess,sys
import argparse,logging

from common.func import bug_HashId
from core.settings import SCAN_PATH

author = "Bing"
version = "V1"


def brute(task_id = "", task_target = "",model = "" , scan_type = "" , cookie = "wukong" , thread_num = 50 ):
    if task_id != "" and task_target != "":
        if scan_type == "":
            cmdline = 'python brute.py -i %s -d %s -m %s -t \"\" -c %s -th %d' % (task_id,task_target,model,cookie,thread_num)
            print cmdline
        else:
            cmdline = 'python brute.py -i %s -d %s -m %s -t %s -c %s -th %d' % (task_id,task_target,model,scan_type,cookie,thread_num)
            print cmdline            
    else:
        pass

    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return process_output


def awvs(task_id = "" , task_target = "" , cookie = "wukong" ):
    if task_id != "" and task_target != "":
        cmdline = 'python awvs.py -i %s -d %s -c %s' % (task_id,task_target,cookie)
        print cmdline
    else:
        pass
    
    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return process_output


def nessus(task_id = "", task_target = "" , cookie = "" ):
    if task_id != "" and task_target != "":
        cmdline = 'python nessus.py -i %s -d %s' % (task_id,task_target)
        print cmdline
    else:
        pass
    
    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return process_output

def pscan(task_id = "", task_target = "" ):
    if task_id != "" and task_target != "":
        cmdline = 'python pscan.py -i %s -d %s' % (task_id,task_target)
        print cmdline
    else:
        pass
    
    nmap_proc = subprocess.Popen(cmdline , shell=True , stdout = subprocess.PIPE , stderr = subprocess.PIPE ,cwd = SCAN_PATH )
    
    process_output = nmap_proc.stdout.readlines()
    return process_output

if __name__ == '__main__':
    usage = """
    _          __  _   _   _   _    _____   __   _   _____  
    | |        / / | | | | | | / /  /  _  \ |  \ | | /  ___| 
    | |  __   / /  | | | | | |/ /   | | | | |   \| | | |     
    | | /  | / /   | | | | | |\ \   | | | | | |\   | | |  _  
    | |/   |/ /    | |_| | | | \ \  | |_| | | | \  | | |_| | 
    |___/|___/     \_____/ |_|  \_\ \_____/ |_|  \_| \_____/ 

                Author: %s && Ver: %s

    For example:
    python wukong.py -d 100.xueersi.com -m pscan        #port scan
    python wukong.py -d 100.xueersi.com -m nessus       #nessus scan
    python wukong.py -d 100.xueersi.com -m awvs         #awvs scan
    python wukong.py -d 100.xueersi.com -m web          #all scan by 0day
    python wukong.py -d 100.xueersi.com -m brute        #all brute by all ports
    python wukong.py -d 100.xueersi.com -m brute -c SESSION=232     #all ports brute by cookie        
    python wukong.py -d 100.xueersi.com -m web -t subdomain     #subdomain scan
    python wukong.py -d 100.xueersi.com -m brute -t subdomain   #subdomain brute
    python wukong.py -d 100.xueersi.com -m all          #scan all        

    """ % (author,version)

    print usage

    taskid = bug_HashId("TASKID")

    parser = argparse.ArgumentParser(description="wukong scanner v 1.0")
    parser.add_argument("-d", "--host",metavar="", default='', help="www.x.com/127.0.0.1")
    parser.add_argument("-m", "--model",metavar="", default='all', help="web/brute/pscan/awvs/nessus/all")
    parser.add_argument("-t", "--type",metavar="", default='', help="subdomain")
    parser.add_argument("-c", "--cookie",metavar="", default='wukong', help="SESSIONID=2H23I2Y2K3YI234H")
    parser.add_argument("-th", "--thread",metavar="", default=50, help="50")
    args = parser.parse_args()

    host = args.host
    model = args.model
    scantype = args.type
    cookie = args.cookie
    threadnum = args.thread

    if host != "" :
        if model == "web" or model == "brute" :
            try:
                result = brute(task_id = taskid, task_target = host,  model = model , scan_type = scantype , cookie = cookie , thread_num = threadnum )
                for line in result:
                    print line.strip()
            except:
                sys.exit(1)

        elif model == "awvs" :
            try:
                result = awvs(task_id = taskid, task_target = host, cookie = cookie )
                for line in result:
                    print line.strip()
            except:
                sys.exit(1)

        elif model == "nessus" :
            try:
                result = nessus(task_id = taskid, task_target = host, cookie = cookie )
                for line in result:
                    print line.strip()
            except:
                sys.exit(1)

        elif model == "pscan" :
            try:
                result = pscan(task_id = taskid, task_target = host )
                for line in result:
                    print line.strip()
            except:
                sys.exit(1)

        elif model == "all" :
            try:
                pscan_result = pscan(task_id = taskid, task_target = host )
                web_result = brute(task_id = taskid, task_target = host,  model = "web" , scan_type = scantype , cookie = cookie , thread_num = threadnum )
                brute_result = brute(task_id = taskid, task_target = host,  model = "brute" , scan_type = scantype , cookie = cookie , thread_num = threadnum )
                awvs_result = awvs(task_id = taskid, task_target = host, cookie = cookie )
                nessus_result = nessus(task_id = taskid, task_target = host, cookie = cookie )
                for line in pscan_result:
                    print line.strip()
                for line in web_result:
                    print line.strip()
                for line in brute_result:
                    print line.strip()
                for line in awvs_result:
                    print line.strip()
                for line in nessus_result:
                    print line.strip()
            except:
                sys.exit(1)
        else:
            pass
    else:
        print parser.print_help()
        sys.exit(1)

