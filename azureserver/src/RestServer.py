import paramiko
import os
class Usage:
    def __init__(self):
        pass
    
class RestServer():
    def __init__(self,path):
        self.labs=set()
        self.lab_vm_dict = dict()
        #self.__get_lab_vm_table()
        self.labs.add('python')
        f = open(path,'r')
        hostname = f.readline().strip()
        username = f.readline().strip()
        password = f.readline().strip()
        port = f.readline().strip()
        vm = {'hostname':hostname,'username':username,'password':password,'port':port}
        hostinfo=[vm]
        self.lab_vm_dict['python']=hostinfo
        f.close()
    
    #TODO
    def __get_lab_vm_table(self):
        #current_dir = os.getcwd()
        os.chdir('../../conf')
        f = open(os.getcwd()+'/lab_vm.dat','r')
        while True:
            line = f.readline()
            
        self.labs.append(f.readline())
        self.virtual_machines.append(f.readline())
    def get_virtual_machine(self,lab):
        if (lab in self.labs)==True:
            vms = self.lab_vm_dict[lab]
            return vms[0]
        else:
            pass
        
    #Later TO DO
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
    client = connect('osslab.chinacloudapp.cn',22,'opentech','@dministrat0r');
    stdin,stdout,stderr = client.exec_command('ls -alh')
    print stdout.read()
    print stderr.read()
    client.close()
    
if __name__=='__main__':
    rs = RestServer()
    host = rs.get_virtual_machine('python')
    print host['hostname']
    print host['username']
    print host['port']
    '''
    client = rs.resource_monitor('osslab.chinacloudapp.cn','opentech','@dministrat0r',22)
    stdin,stdout,stderr = client.exec_command('ls -alh')
    #stdin.write('oliverkahnno.1\n')
    #stdin.flush()
    print stdout.read()
    print stderr.read()
    client.close()
    '''
    
    
    