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
            res.status = 0
            res.image = ''
            session.commit()
            protocol = res.protocol
            guacamole_server = res.guacamole_server
            query = session.query(GuacamoleServerLoad)
            result = query.filter(GuacamoleServerLoad.guacamole_server == guacamole_server).first()
            if result.server_load>=1:
                result.server_load -= 1
            if protocol=='vnc':
                result.vnc_count += 1
            elif protocol=='vnc-readonly':
                result.vnc_readonly_count += 1
            elif protocol=='ssh':
                result.ssh_count += 1
            else:
                result.rdp_count += 1
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
        zlt = res.zero_load_timestamp
        zlt = zlt[0:zlt.index('.')]
        t = time.strptime(zlt,'%Y-%m-%d %H:%M:%S')
        zero_load_timestamp = datetime(*t[:6])
        seconds = (cur_time-zero_load_timestamp).seconds
        if seconds
        
        
        
        