import paramiko
import os
class RestServer():
    def __init__(self):
        self.labs=[]
        self.virtual_machines=[]
        self.lab_vm_table = {}
        self.__get_lab_vm_table()
        
    def __get_lab_vm_table(self):
        #current_dir = os.getcwd()
        os.chdir('../../conf')
        f = open(os.getcwd()+'/lab_vm.conf','r')
        self.labs.append(f.readline())
        self.virtual_machines.append(f.readline())
    
    #later to do
    def resource_monitor(self,host,username,password,port):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password);
            return client
        except Exception, e:
            print 'Error Connecting : '+str(e)
        

def connect(hostname,port=22,username=None,password=None):
    pass

def test():
    client = connect('kangjihua.chinacloudapp.cn',22,'kangjihua','oliverkahnno.1');
    stdin,stdout,stderr = client.exec_command('sudo find / -name \.vnc')
    #stdin.write('oliverkahnno.1\n')
    #stdin.flush()
    print stdout.read()
    print stderr.read()
    client.close()
    
if __name__=='__main__':
    rs = RestServer()
    print rs.labs
    print rs.virtual_machines
    
    
    