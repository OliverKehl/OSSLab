'''
@author: kehl
@contact: t-jikang@microsoft.com
'''

import thread
from xml.etree.ElementTree import ElementTree

class Guaca:
    status = 0
    labname = ''
    hostname = ''
    #port = 0 # port number should be an integer
    guacname=''
    guacamole_url=''
    def __init__(self,labname,hostname,guacname):
        self.labname = labname
        self.hostname = hostname
        #self.port = port
        self.guacname = guacname
        self.guacamole_url = self.hostname+'client.xhtml?id=c/'+self.guacname
        self.status = 0 # 0 means available

'''
@todo: use a status info to record current GuacamoleServer status, so that when a user is asking for a server, the rest serve
       does'nt need to scan all the guacamole server, but just use the status info to determine use which GuacamoleServer to allocate guaca
'''
class GuacamoleServer:
    #guaca_list,  key:labname  value: list of Guaca
    guaca_dict=dict()
    lock = thread.allocate_lock()
    def __init__(self,config_file):
        #initialize the guaca_list with config_file
        self.lock.acquire()
        self.read_config(config_file)
        self.status=0
        self.lock.release()
        
    def read_config(self,config_file):
        tree = ElementTree()
        tree.parse(config_file)
        root = tree.getroot()
        labs = root.getchildren()
        for lab in labs:
            labname = lab.attrib['name']
            host = lab[0].text
            guacname = lab[1].text
            if labname not in self.guaca_dict.keys():
                self.guaca_dict[labname]=[]
            guaca = Guaca(labname,host,guacname)
            self.guaca_dict[labname].append(guaca)
    
    def invoke_guaca(self,lab):
        self.lock.acquire()
        if lab not in self.guaca_dict.keys():
            self.lock.release()
            return None
        candidates = self.guaca_dict[lab]
        for cand in candidates:
            if cand.status==0:
                cand.status = 1
                self.lock.release()
                return cand.guacamole_url
        self.lock.release()
        return None
    
    def revoke_guaca(self,lab,guacamole_url):
        if lab not in self.guaca_dict.keys():
            return
        candidates = self.guaca_dict[lab]
        for cand in candidates:
            if cand.guacamole_url==guacamole_url:
                cand.status = 0
        

if __name__=='__main__':
    g = GuacamoleServer('/home/kehl/workspace/OSSLab/conf/guacamole_server.xml')
    