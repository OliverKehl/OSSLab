import web,json
import test
import AzureService
urls = ('/(.*)', 'index')
class index:
    def GET(self,tag):
        #do some thingi 
        web.input(tag=None)
        if tag=='python':
            #get virtual machine list for python
            #vm_list = get_
            #check virtual machine status
            #get_virtual_machine_status()
            azureservice = AzureService.AzureService()
            pyDict = {'hostname':'khost','username':'kangjihua','password':'opentech','port':'8080'}
            web.header('Content-Type', 'application/json')
            azureservice.create_linux_vm('kangjihua','kangjihua')
            return json.dumps(pyDict)
        else:
            return 'Hello world'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()