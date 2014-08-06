#coding=utf-8
import web,json,restserver,thread
urls = ('/(.*)', 'index')
rs = restserver.RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml','/home/kehl/workspace/OSSLab/conf/authentication.xml')
lock = thread.allocate_lock()
class index:
    global lock
    def __init__(self):
        pass
        
    def parse(self,uri):
        '''
        uri[0]:tag
        uri[1]:lab
        uri[2]:connection type
        '''
        global rs
        if uri[0]=='1':#ask for a server
            if(len(uri)!=3):
                return -1;
            vm = rs.get_virtual_machine_by_lab(uri[1])
            return 1
            if vm==None:
                return -1
        elif uri[0]=='2':#record the PID, the session and the host name
            if(len(uri)!=6):
                return -1;
            #client_id, host name, port, pid, lab name
            result = rs.record_user_virtual_machine_info(uri[1],uri[2],uri[3],uri[4],uri[5])
            if result==True:
                return 2
            return -1
        elif uri[0]=='3':#quit and clear the screen session
            if(len(uri)!=3):
                return -1
            rs.quit_screen(uri[1], uri[2])
            return 3
        elif uri[0]=='4':
            #re-load the rest server
            rs.reload_config('', '')
            return 4
        else:
            return -1

    def GET(self,info):
        web.input(info=None)
        #shit=web.ctx.items()
        #print shit
        info = str(info)
        info = info.split('_')
        print info
        result = self.parse(info)
        if result==1:
            pyDict = rs.get_virtual_machine_by_lab(info[1])
            web.header('Content-Type', 'application/json')
            return json.dumps(pyDict)
        elif result==2:
            pass
        elif result==3:
            pass
        elif result==4:
            return rs.fuck
        else:
            return 'Illegal Request'
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()