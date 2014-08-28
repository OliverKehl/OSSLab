from ormConnection import DBSession,init_session
from tables  import GuacamoleClientInfo,GuacamoleServerLoad
from datetime import datetime
import time
import restserver

init_session()

def reset_guacamole_client():
    session = DBSession()
    query = session.query(GuacamoleClientInfo)
    result = query.filter(GuacamoleClientInfo.status==1).filter(GuacamoleClientInfo.user_info!='').with_lockmode('update').all()
    if result==None:
        return
    cur_time = datetime.now()
    for res in result:
        lat = str(res.latest_active_timestamp)
        #lat = lat[0:lat.index('.')]
        t = time.strptime(lat,'%Y-%m-%d %H:%M:%S')
        latest_active_time = datetime(*t[:6])
        seconds = (cur_time-latest_active_time).seconds
        if seconds>=20: # 2 hours
            res.user_info = ''
            res.status = 0
            res.image = ''
            protocol = res.protocol
            guacamole_server = res.guacamole_server
            query = session.query(GuacamoleServerLoad)
            result = query.filter(GuacamoleServerLoad.guacamole_server == guacamole_server).with_lockmode('update').first()
            result = restserver.server_protocol_update(protocol,-1,result)
        #TODO(): need to shutdown and remove the container
    session.commit()
    session.close()
    
'''
Since this method will lock the table(temporarily) coarse grained, it should be called in some idle period  
'''
def remove_guacamole_server():
    session = DBSession()
    try:
        session.execute('LOCK TABLES guacamole_client_info WRITE,guacamole_server_load WRITE')
        query = session.query(GuacamoleServerLoad)
        result = query.filter(GuacamoleServerLoad.server_load==0).all()
        if result==None:
            return
        cur_time = datetime.now()
        query = session.query(GuacamoleClientInfo)
        for res in result:
            zlt = str(res.zero_load_timestamp)
            #zlt = zlt[0:zlt.index('.')]
            t = time.strptime(zlt,'%Y-%m-%d %H:%M:%S')
            zero_load_timestamp = datetime(*t[:6])
            seconds = (cur_time-zero_load_timestamp).seconds
            if seconds>10:#2 hours
                #remove all the client_info heading to this server
                query.filter(GuacamoleClientInfo.guacamole_server==res.guacamole_server).delete()
            session.delete(res)
            session.commit()
    except Exception,e:
        print e
        session.rollback()
    finally:
        session.execute('UNLOCK TABLES')
        session.close()
        
if __name__=='__main__':
    #reset_guacamole_client()
    remove_guacamole_server()
    #session = DBSession()
    #session.execute('lock tables guacamole_client_info write')
    #time.sleep(100)
    #query = session.query(GuacamoleClientInfo)
    #res = query.filter(GuacamoleClientInfo.protocol=='vnc').with_lockmode('read').first()

    #time.sleep(1000)
    #session.commit()
    
        
        
        