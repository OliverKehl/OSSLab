#coding=utf-8
import paramiko
from xml.etree.ElementTree import ElementTree
class Usage:
    def __init__(self):
        pass
    
class RestServer():
    def __init__(self,path):
        self.__lab_set=set()
        self.__lab_virtual_machine_dict = dict()
        self.__user_virtual_machine_dict = dict()
        self.__read_config(path)
        self.__max_iter=100
    
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
            if (lab_name in self.__lab_set) ==False:
                self.__lab_set.add(lab_name)
                self.__lab_virtual_machine_dict[lab_name]=[]
            vms = lab.findall('host')
            for vm in vms:
                tmp={}
                info = vm.getchildren()
                for i in range(len(info)):
                    tmp[info[i].tag] = info[i].text
                self.__lab_virtual_machine_dict[lab_name].append(tmp)
        
    def get_virtual_machine(self,lab):
        if (lab in self.__lab_set)==True:
            vms = self.__lab_virtual_machine_dict[lab]
            vms[0]['lab']=lab
            return vms[0]
        else:
            return None
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
    #Later TO DO
    def resource_monitor(self,host,username,password,port):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password);
            return client
        except Exception, e:
            print 'Error Connecting : '+str(e)
    
    def record_user_virtual_machine_info(self,info):
        #client_id,hostname,pid,lab_name
        self.__user_virtual_machine_dict[info[0]] = info[1:]
        return True
    def __check_process_existence(self,client,pid):
        stdin,stdout,stderr = client.exec_command('ps -p '+str(pid)+' -f | grep '+str(pid))
        res = stdout.read()
        if len(res)>0:
            return True
        return False
        
    def kill_process(self,client_id):
        #get the host name, username, password and port
        #kill the pid with paramiko
        #if any exception, iter this flow for no more than self.__max_iter times
        hostname=None
        username=None
        password=None
        port = None
        pid=None
        client = self.__create_ssh_client(hostname, username, password, port)
        cur_iter=0
        while client==None and cur_iter<self.__max_iter:
            client = self.__create_ssh_client(hostname, username, password, port)
            cur_iter = iter+1
        cur_iter = 0
        while True and cur_iter<self.__max_iter:
            client.exec_command('kill '+pid)
            pid_existence = self.__check_process_existence(client, pid)
            cur_iter = iter+1
            if pid_existence==False:
                break
        client.close()
    
if __name__=='__main__':
    rs = RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml')
    
    host = rs.get_virtual_machine('python')
    print host['lab']
    print host['hostname']
    print host['username']
    print host['port']
    rs.kill_process(16666)
    
    
    