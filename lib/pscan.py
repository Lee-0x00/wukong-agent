#!/user/bin python
# -*- coding:utf-8 -*- 
# Author:Bing
# Contact:amazing_bing@outlook.com
# DateTime: 2017-01-17 19:06:06
# Description:  coding 

import sys
sys.path.append("..")

import threading, socket, Queue,argparse,logging

from core.settings import DICT_PATH,save_result    #configure


#threading lock
lock = threading.Lock()

#make queue for port
def GetQueue(host):
    PortQueue = Queue.Queue()
    for port in range(1,65535):
        PortQueue.put((host,port))
    return PortQueue

class ScanThread(threading.Thread):
    def __init__(self,SingleQueue,outip):
        threading.Thread.__init__(self)
        self.setDaemon(True)		#set daemon process
        self.SingleQueue = SingleQueue
        self.outip = outip

    def get_port_service(self,text):
        service_path = DICT_PATH+"nmap-services.txt"
        port_server = str(text)+"/tcp"
        with open(service_path,"r") as server:
            for finger in server.readlines():
                port = finger.strip().split(";")[1]
                if port == port_server:
                    fingers = str(finger.strip().split(";")[0])
                    return (port_server,fingers)
            return (port_server,"unknown")

    def Ping(self,scanIP, Port):
        global lock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        address = (scanIP, Port)
        try:
            sock.connect(address)
        except:
            sock.close()
            return False
        sock.close()

        lock.acquire()
        self.outip.put(self.get_port_service(Port))
        lock.release()
        return True

    def run(self):
        while not self.SingleQueue.empty():
            host,port = self.SingleQueue.get()
            self.Ping(host,port)


class Work(object):
    def __init__(self, task_id = "", task_target = "", model = "" , scan_type = "", thread_num = 200 ):
        self.task_id = task_id
        self.task_target = task_target
        self.model = model
        self.scan_type = scan_type
        self.thread_num = int(thread_num)
        self.result = []  
      

    def run(self):
        ThreadList = []
        #scan queue
        SingleQueue = GetQueue(self.task_target)
        #result queue
        resultQueue = Queue.Queue()
        #startup thread concurrency
        for i in range(0, self.thread_num):
            t = ScanThread(SingleQueue,resultQueue)
            ThreadList.append(t)
        for t in ThreadList:
            t.start()
        for t in ThreadList:
            #set subprocess timeout
            t.join(2)

        while not resultQueue.empty():
            result = resultQueue.get() 
            task_result = {
                "task_id": self.task_id , 
                "bug_model": self.model ,
                "bug_type" : self.scan_type,
                "bug_author" : "bing",
                "bug_name" : result[0] ,
                "bug_level" : "",
                "bug_summary" : result[1] ,
                "bug_detail" : "" ,
                "bug_repair" : ""
            }
            save_result(self.model,task_result)
            self.result.append(task_result)

        #finish
        final_result = { "status" : 1 , "task_id": self.task_id , "bug_model": self.model }
        save_result(self.model,final_result)
        self.result.append(final_result)


if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description="wukong scanner v 1.0")
    parser.add_argument("-i", "--id",metavar="", default='', help="TASKID-20170817-783554")
    parser.add_argument("-d", "--host",metavar="", default='', help="www.x.com/127.0.0.1")

    args = parser.parse_args()

    taskid = args.id
    host = args.host

    if host != "" :
        try:
            t = Work(task_id = taskid , task_target = host , model = "pscan" , thread_num = 100)
            t.run()
            for line in t.result :
                print line
        except:
            print parser.print_help()
            sys.exit(1)
    else:
        print parser.print_help()
        sys.exit(1)


