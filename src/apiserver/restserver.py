#coding=utf-8
import paramiko,datetime,thread
from xml.etree.ElementTree import ElementTree
    
class RestServer():
    def __init__(self,lab_vm_path,host_authentication_path):
        self.__lock = thread.allocate_lock()
        self.__max_iter=100
        self.created_time = datetime.datetime.now()
        
        self.__lab_set=set()
        self.__lab_virtual_machine_dict = dict()
        self.__virtual_machine_guacamole_dict = dict()
        self.__session_virtual_machine_dict = dict()
        
        self.__read_lab_vm_config(lab_vm_path)              
        
    def __read_lab_vm_config(self,path):
        '''
        init the lab_virtual_machine_dict, virtual_machine_guacamole_dict 
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
                for guacamole in host:
                    guacamole_name = guacamole.attrib['name']
                    
                    #lab_virtual_machine_dict
                    vm_info = dict()
                    vm_info['host'] = host_name
                    for item in guacamole:
                        vm_info[item.tag] = item.text
                    self.__lab_virtual_machine_dict[lab_name].append(vm_info)              
                    
                    #virtual_machine_guacamole
                    self.__virtual_machine_guacamole_dict[host_name+'_'+vm_info['port']+'_'+lab_name] = guacamole_name
    
    def __create_ssh_client(self,host,username,password,port):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password)
            #return client
        except Exception,e:
            print 'Error Connecting : '+str(e)
            client=None
        finally:
            return client
    
    def __check_session_existence(self,client_id,lab_name):
        '''
        actually 'lab' here is something duplicate
        the lab information shall be covered by the 'client_id'
        return the virtual machine for the client_id
        '''
        if self.__session_virtual_machine_dict.has_key(client_id+'_'+lab_name)==True:
            vm = self.__session_virtual_machine_dict[client_id+'_'+lab_name]
            return vm
            #return self.__virtual_machine_guacamole_dict[vm['host']+'_'+vm['port']+'_'+lab_name]
        return None
    
    def __get_virtual_machine_status(self,host,port,username,password):
        client = self.__create_ssh_client(host, username, password, port)
        output = client.exec_command('/usr/bin/python2 /tmp/moniter_script.py')
        status = output[1].read().strip()
        client.close()
        if status=='0':
            return True
        return False
    
    def __get_virtual_machine_by_lab(self,client_id,lab_name):
        if (lab_name in self.__lab_set)==True:
            vms = self.__lab_virtual_machine_dict[lab_name]
            for vm in vms:
                host = vm['host']
                port = int(vm['port'])
                username = vm['username']
                password = vm['password']
                status = self.__get_virtual_machine_status(host, port, username, password)
                
                if status==True:#OK
                    self.__session_virtual_machine_dict[client_id+'_'+lab_name] = vm
                    return vm
                #what if all the vm status are not OK?
        else:
            #should do something to prevent this, there is no class here
            return None
        return None
      
    def get_guacamole(self,client_id,lab_name):
        vm = self.__get_virtual_machine_by_lab(client_id, lab_name)
        if vm==None:
            return None
        return self.__virtual_machine_guacamole_dict[vm['host']+'_'+vm['port']+'_'+lab_name]
        
    def modify_profile(self,client_id,lab_name,vm):
        host = vm['host']
        port = int(vm['port'])
        username = vm['username']
        password = vm['password']
        client = self.__create_ssh_client(host, username, password, int(port))
        while True:
            output = client.exec_command('find /tmp/id_log')
            result = output[1].read().strip()
            if len(result)==0:#non-exist
                self.__lock.acquire()
                client.exec_command('echo '+client_id+'_'+lab_name+' >/tmp/id_log')
                self.__lock.release()
                break
        
    def reload_config(self,lab_vm_path,authentication_path):
        self.__lab_set=set()
        self.__lab_virtual_machine_dict = dict()
        self.__read_lab_vm_config(lab_vm_path)
        
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
    
    def quit_screen(self,client_id,screen_name):
        hostname,port,pid,lab_name = self.get_virtual_machine_info(client_id)
        username,password = self.__get_virtual_machine_authentication(hostname,port)
        client = self.__create_ssh_client(hostname, username, password, int(port))
        stdin,stdout,stderr = client.exec_command('screen -X -S '+screen_name+' quit')
    
    #Later TO DO
    def resource_monitor(self,host,username,password,port):
        pass

if __name__=='__main__':
    rs = RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml','/home/kehl/authentication.xml')
    host = rs.get_guacamole('kangjihua', 'python')
    print host['host']
    print host['username']
    print host['password']
    print host['port']
    #rs.kill_process(16666)
    
    
    