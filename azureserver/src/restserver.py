#coding=utf-8
import paramiko,datetime
from xml.etree.ElementTree import ElementTree
class Usage:
    def __init__(self):
        pass
    
class RestServer():
    def __init__(self,lab_vm_path,host_authentication_path):
        self.__lab_set=set()
        self.__lab_virtual_machine_dict = dict()
        self.__host_authentication_dict = dict()
        self.__user_virtual_machine_dict = dict()
        self.__read_lab_vm_config(lab_vm_path)
        self.__read_host_authentication_config(host_authentication_path)
        self.__max_iter=100
        self.created_time = datetime.datetime.now() 
    
    def __read_host_authentication_config(self,path):
        '''
        '''
        tree = ElementTree()
        tree.parse(path)
        root = tree.getroot()
        hosts = root.getchildren()
        for host in hosts:
            host_name = host.attrib['name']
            for role in host:
                vm = host_name
                auth=dict()
                for item in role:
                    if item.tag=='port':
                        vm = vm + ':' + item.text
                    else:
                        auth[item.tag] = item.text
                self.__host_authentication_dict[vm] = auth
        
    def __read_lab_vm_config(self,path):
        '''
        Initial the lab and virtual machine map
        '''
        tree = ElementTree()
        tree.parse(path)
        root = tree.getroot()
        labs = root.getchildren()
        for lab in labs:
            lab_name = lab.attrib['name']
            if (lab_name in self.__lab_set) ==False:
                self.__lab_set.add(lab_name)
                self.__lab_virtual_machine_dict[lab_name]=[]
            for host in lab:
                host_name = host.attrib['name']
                for port in host:
                    virtual_machine = dict()
                    virtual_machine['hostname'] = host_name
                    virtual_machine['port'] = port.text
                    self.__lab_virtual_machine_dict[lab_name].append(virtual_machine)
    
    def __check_process_existence(self,client,pid):
        stdin,stdout,stderr = client.exec_command('ps -p '+str(pid)+' -f | grep '+str(pid))
        res = stdout.read()
        if len(res)>0:
            return True
        return False
        
    def __create_ssh_client(self,host,username,password,port):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password);
            #return client
        except Exception,e:
            print 'Error Connecting : '+str(e)
            client=None
        finally:
            return client
         
    def __get_virtual_machine_authentication(self,hostname,port):
        '''
        Return the username and password according to the hostname and port 
        '''
        return 'opentech','@dministrat0r'
    
    def get_virtual_machine_by_lab(self,lab):
        if (lab in self.__lab_set)==True:
            vms = self.__lab_virtual_machine_dict[lab]
            whole_host_name = vms[0]['hostname']+':'+vms[0]['port']
            #hard code
            #return the first virtual machine
            #actually I need to check the status and usage for all the candidate virtual machines
            # and then pick one of them 
            temp = self.__host_authentication_dict[whole_host_name] 
            vms[0]['lab']=lab
            vms[0].update(temp)
            return vms[0]
        else:
            return None
    
    def record_user_virtual_machine_info(self,client_id,hostname,port,pid,lab_name):
        #client_id,hostname,port,pid,lab_name
        if client_id in self.__user_virtual_machine_dict:
            return False
        info = dict()
        info['hostname'] = hostname
        info['port'] = port
        info['pid'] = pid
        info['lab_name'] = lab_name 
        self.__user_virtual_machine_dict[client_id] = info
        return True
    
    def get_virtual_machine_info(self,client_id):
        tmp = self.__user_virtual_machine_dict[client_id]
        return tmp['hostname'],tmp['port'],tmp['pid'],tmp['lab_name']
    
    def kill_process(self,client_id):
        '''
        Get the host name, username, password and port by client_id
        Kill the pid with paramiko
        If any exception, iter this flow for no more than self.__max_iter times
        '''

        hostname,port,pid,lab_name = self.get_virtual_machine_info(client_id)
        username,password = self.__get_virtual_machine_authentication(hostname,port)
        
        client = self.__create_ssh_client(hostname, username, password, int(port))
        cur_iter=0
        while client==None and cur_iter<self.__max_iter:
            client = self.__create_ssh_client(hostname, username, password, port)
            cur_iter = iter+1
        cur_iter = 0
        while True and cur_iter<self.__max_iter:
            client.exec_command('kill '+pid)
            pid_existence = self.__check_process_existence(client, pid)
            cur_iter = cur_iter+1
            if pid_existence==False:
                break
        client.close()

    #Later TO DO
    def resource_monitor(self,host,username,password,port):
        pass

if __name__=='__main__':
    rs = RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml','/home/kehl/authentication.xml')
    host = rs.get_virtual_machine_by_lab('python')
    print host['lab']
    print host['hostname']
    print host['username']
    print host['password']
    print host['port']
    #rs.kill_process(16666)
    
    
    