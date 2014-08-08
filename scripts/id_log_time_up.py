import time,os    

def time_up():
    path = r'/tmp/id_log'
    while True:
        if os.path.exists(path)==False:
            time.sleep(3)
            continue
        created_time = (float)(os.path.getctime(path))
        current_time = (float)(time.time())
        if current_time-created_time>=5.0:
            os.remove(path)
        time.sleep(3)

if __name__=='__main__':
    time_up()