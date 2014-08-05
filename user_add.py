import os,crypt,commands

def check_user(username):
    status,output = commands.getstatusoutput('cat /etc/passwd')
    if status!=0:
        return False
    users = output.split('\n')
    for u in users:
        if username==u[0:u.index(':')]:
            return True
    return False

def add_user(sudoPassword,username,password):
    #echo "552523" | sudo useradd -d /home/guest -m -s /bin/bash -g users guest
    status,output = commands.getstatusoutput('echo 552523 | sudo -S userdel -r guest 1>>output.log 2>>error.log')
    print output
    status,output = commands.getstatusoutput('echo 552523 | sudo -S useradd -d /home/guest -m -s /bin/bash -g users guest')
    print output
    passwd=crypt.crypt('123456','ab')
    status,output = commands.getstatusoutput('echo 552523 | sudo -S usermod -p '+passwd+' guest')
    print output
    status,output = commands.getstatusoutput('echo 123456 | su - guest echo python >> /home/guest/.profile')
    print output
    status,output = commands.getstatusoutput('echo 123456 | sudo -u guest source /home/guest/.profile')
    print output
    
    '''
    os.system('echo 552523 | sudo -S userdel -r guest 1>>output.log 2>>error.log')
    os.system('echo 552523 | sudo -S useradd -d /home/guest -m -s /bin/bash -g users guest')
    passwd=crypt.crypt('123456','ab')
    os.system('echo 552523 | sudo -S usermod -p '+passwd+' guest')
    #os.system('echo 552523 | su guest')
    os.system('echo python >> /home/guest/.profile')
    os.system('source /home/guest/.profile')
    '''
def modify_profile(username):    
    os.system('sudo chmod 666 /home/'+username+'/.profile')
    
    
    
if __name__=='__main__':
    check_user('guest')
    #add_user('123','123','123')