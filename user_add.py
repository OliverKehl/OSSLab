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
    os.system('echo '+sudoPassword+ ' | sudo -S userdel -r '+username+' 1>>output.log 2>>error.log')
    os.system('echo '+sudoPassword+ ' | sudo -S useradd -d /home/'+username+' -m -s /bin/bash -g users '+username)
    passwd=crypt.crypt(password,'ab')
    os.system('echo '+sudoPassword+ '| sudo -S usermod -p '+passwd+' '+username)
    
    #may need to modify the .profile for the new added user
    =================================================
    
def modify_profile(username):    
    os.system('sudo chmod 666 /home/'+username+'/.profile')
    
    
    
if __name__=='__main__':
    check_user('guest')
    #add_user('123','123','123')