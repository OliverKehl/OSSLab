import web,json
import AzureService,RestServer
urls = ('/(.*)', 'index')



class index:
    def __init__(self):
        pass
    def GET(self,info):
        #do some thingi
        self.restserver = RestServer.RestServer('/home/kehl/temp.dat') 
        web.input(info=None)
        info = info.split('_')
        if len(info)>1 and info[0]=='python':
            #get virtual machine list for python
            #vm_list = get_
            #check virtual machine status
            #get_virtual_machine_status()
            #azureservice = AzureService.AzureService()
            
            if info[1]=='1':#share one desktop
                pass
            else:#give the user control
                pass
            pyDict = self.restserver.get_virtual_machine(info[0])
            web.header('Content-Type', 'application/json')
            return json.dumps(pyDict)
        else:
            return 'Illegal Request'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()