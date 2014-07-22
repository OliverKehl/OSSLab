#coding=utf-8
import web,json,restserver
urls = ('/(.*)', 'index')

class index:
    def __init__(self):
        self.restserver = restserver.RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml')
    def parse(self,uri):
        '''
        uri[0]:tag
        uri[1]:lab
        uri[2]:connection type
        '''
        if uri[0]=='1':#ask for a server
            if(len(uri)!=3):
                return -1;
            
            return 1
        elif uri[0]=='2':#record the PID, the session and the host name
            if(len(uri)!=5):
                return -1;
            result = self.restserver.record_user_virtual_machine_info(uri[1:5])
            if result==True:
                return 2
            return -1
        elif uri[0]=='3':#receive a shutdown signal and kill the PID correspond to the session
            if(len(uri)!=2):
                return -1
            
            return 3
        else:
            return -1
        
    def GET(self,info):
        #do some thingi
        web.input(info=None)
        info = str(info)
        print info
        info = info.split('_')
        print info
        result = self.parse(info)
        if result==True:
            pyDict = self.restserver.get_virtual_machine(info[0])
            web.header('Content-Type', 'application/json')
            return json.dumps(pyDict)
        else:
            return 'Illegal Request'
        #if pyDict==None:
            #create a virtual machine and record it into the lab_vm.xml 
         #   pass
            

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()