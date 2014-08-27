from ormConnection import DBSession,init_session
from tables  import GuacamoleClientInfo,GuacamoleServerLoad
from datetime import datetime
import time
import restserver

init_session()

def reset_guacamole_client():
    session = DBSession()
    query = session.query(GuacamoleClientInfo)
    result = query.filter(GuacamoleClientInfo.status==1).filter(GuacamoleClientInfo.user_info!='').all()
    if result==None:
        return
    cur_time = datetime.now()
    for res in result:
        lat = str(res.latest_active_timestamp)
        #lat = lat[0:lat.index('.')]
        t = time.strptime(lat,'%Y-%m-%d %H:%M:%S')
        latest_active_time = datetime(*t[:6])
        seconds = (cur_time-latest_active_time).seconds
        if seconds>=10: # 2 hours
            res.user_info = ''
            res.status = 0
            res.image = ''
            session.commit()
            protocol = res.protocol
            guacamole_server = res.guacamole_server
            query = session.query(GuacamoleServerLoad)
            result = query.filter(GuacamoleServerLoad.guacamole_server == guacamole_server).first()
            result = restserver.server_protocol_update(protocol,-1,result)
            session.commit()
    session.close()
    
    
def remove_guacamole_server():
    restserver.guacamole_client_lock.acquire()
    
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
        if seconds>7200:
            pass
        
    restserver.guacamole_client_lock.release()
        
def test():
    #reset_guacamole_client()
    
    session1 = DBSession()
    session2 = DBSession()
    query1 = session1.query(GuacamoleClientInfo)
    query2 = session2.query(GuacamoleClientInfo)
    #res1 = query1.filter(GuacamoleClientInfo.guacamole_client_name=='myvnc').with_lockmode('update').first()
    res1 = query1.filter(GuacamoleClientInfo.guacamole_client_name=='myvnc').filter(GuacamoleClientInfo.protocol=='vnc').with_lockmode('update').first()
    session1.rollback()
    print '***********************************'
    #res2 = query2.filter(GuacamoleClientInfo.guacamole_client_name=='myssh').with_lockmode('update').first()
    res2 = query2.filter(GuacamoleClientInfo.guacamole_client_name=='myvnc').filter(GuacamoleClientInfo.protocol=='vnc').with_lockmode('update').first()
    #res.user_info = 'xia'
    #time.sleep(100)
    res1.user_info = ''
    res2.user_info = ''
    session1.commit()
    print '========================================'
    session2.commit()
    print res1
    print res2

if __name__=='__main__':
    session = DBSession()
    query = session.query(GuacamoleClientInfo)
    result = query.filter(GuacamoleClientInfo.status==0).filter(GuacamoleClientInfo.user_info=='').with_lockmode('update').first()
    result.user_info = 'ri'
    query = session.query(GuacamoleServerLoad)
    result = query.with_lockmode('update').first()
    result = restserver.server_protocol_update('ssh',-1,result)
    session.commit()
    session.close()
        
        
        