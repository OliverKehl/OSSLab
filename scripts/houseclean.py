from ormConnection import DBSession
from tables  import GuacamoleClientInfo,GuacamoleServerLoad
from datetime import datetime
import time

def reset_guacamole_client():
    session = DBSession()
    query = session.query(GuacamoleClientInfo)
    result = query.filter(GuacamoleClientInfo.status==0).all()
    if result==None:
        return
    cur_time = datetime.now()
    for res in result:
        lat = res.latest_active_timestamp
        lat = lat[0:lat.index('.')]
        t = time.strptime(lat,'%Y-%m-%d %H:%M:%S')
        latest_active_time = datetime(*t[:6])
        seconds = (cur_time-latest_active_time).seconds
        if seconds>=7200: # 2 hours
            res.user_info = ''
    session.commit()
    session.close()
        
        
        
    
    
    
def remove_guacamole_server():
    session = DBSession()
    query = session.query(GuacamoleClientInfo)
    result = query.filter(GuacamoleServerLoad.count==0).all()
    if result==None:
        return
    cur_time = datetime.now()
    for res in result:
        
        
        