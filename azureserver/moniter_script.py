import commands
def monitor_all_cpu_usage():
    status,output = commands.getstatusoutput('top -n 1 -bi')
    if status!=0:
        return -1
    info = output.split('\n')[2]
    cpu_info = info.split('  ')[1:]
    for c in cpu_info:
        if c.index('id')>=0:
            return 1-(float(c[0:c.index(' ')]))/100
    
    
def monitor_all_memory_usage():
    status,output = commands.getstatusoutput('top -n 1 -bi')
    if status!=0:
        return -1
    info = output.split('\n')[3]
    mem_info = info.split('  ')[1:]
    

def monitor_all_net_usage():
    pass

def kill_exausted_process():
    pass

if __name__=='__main__':
    print monitor_all_memory_usage()