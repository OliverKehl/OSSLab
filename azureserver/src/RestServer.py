import paramiko,os
from xml.etree.ElementTree import ElementTree
class Usage:
    def __init__(self):
        pass
    
class RestServer():
    def __init__(self,path):
        
        self.labs=set()
        self.lab_vm_dict = dict()
        #self.__get_lab_vm_table()
        '''
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
        '''
        self.__read_config(path)
    
    def __read_config(self,path):
        '''
        initial the lab and virtual machine map
        '''
        tree = ElementTree()
        tree.parse(path)
        root = tree.getroot()
        labs = root.getchildren()
        for lab in labs:
            lab_name = lab.attrib['name']
            if (lab_name in self.labs) ==False:
                self.labs.add(lab_name)
                self.lab_vm_dict[lab_name]=[]
            vms = lab.findall('host')
            for vm in vms:
                tmp={}
                info = vm.getchildren()
                for i in range(len(info)):
                    tmp[info[i].tag] = info[i].text
                self.lab_vm_dict[lab_name].append(tmp)
        
    def get_virtual_machine(self,lab):
        if (lab in self.labs)==True:
            vms = self.lab_vm_dict[lab]
            return vms[0]
        else:
            return None
        
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
    rs = RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml')
    
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
    
    
    