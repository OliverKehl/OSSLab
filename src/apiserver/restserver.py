# coding=utf-8
import thread
from datetime import datetime
from xml.etree.ElementTree import ElementTree
from ormConnection import DBSession
from tables import GuacamoleClientInfo, GuacamoleServerLoad
import guacamoleserver
'''
@author: kehl
@contact: t-jikang@microsoft.com
@version: 0.0

First version with guacamole_server information stored in memory but not in database
'''
class RestServer():
    lock = thread.allocate_lock()
    lock2 = thread.allocate_lock()
    def __init__(self):
        pass
    
    def __server_protocol_update(self,protocol,gain,result):
        if protocol=='ssh':
            result.ssh_count -= gain
        elif protocol=='vnc':
            result.vnc_count -= gain
        elif protocol=='vnc-readonly':
            result.vnc_readonly_count -= gain
        else:
            result.rdp_count -= gain
        result.server_load += gain
        return result
    
    def heart_beat(self, client_id, image):
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == client_id).filter(GuacamoleClientInfo.image == image).first()
        if result != None:
            result.status = 1
            result.latest_active_timestamp = str(datetime.now())
            session.commit()
        session.close()
        
    def get_guacamole_client(self, client_id, image,protocol):
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == client_id).filter(GuacamoleClientInfo.image == image).first()
        if result != None:
            if result.status == 0:
                result.status = 1
            result.latest_active_timestamp = str(datetime.now())
            guacamole_server = result.guacamole_server
            guacamole_client_name = result.guacamole_client_name
            guacamole_client = guacamole_server+'client.xhtml?id=c/'+guacamole_client_name
            session.commit()
            session.close()
            return guacamole_client
        else:
            session.close()
            res = self.establish_guacamole_client(client_id, image,protocol)
            if res != None:
                return res
            self.create_guacamole_server(client_id, image,protocol)
            return self.get_guacamole_client(client_id, image,protocol)
    
    def reset_guacamole_client(self, client_id, image):
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == client_id).filter(GuacamoleClientInfo.image == image).first()
        if result == None:
            return
        #TODO(): House cleaning, shutdown and remove the container with the 'guacamole_client_host' information
        guacamole_client_host = result.guacamole_client_host
        guacamole_server = result.guacamole_server
        protocol = result.protocol
        result.status = 0
        result.user_info = ''
        result.image = ''
        session.commit()
        
        query = session.query(GuacamoleServerLoad)
        result = query.filter(GuacamoleServerLoad.guacamole_server == guacamole_server).first()
        result = self.__server_protocol_update(protocol, -1 , result)
        session.commit()
    
    def establish_guacamole_client(self, client_id, image, protocol=None):
        self.lock.acquire()
        session = DBSession()
        query = session.query(GuacamoleClientInfo)
        #TODO(): if the protocol is None, then I should specify the protocol with my map or DB.
        if protocol == None:
            result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.image == '').first()
        else:
            result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.image == '').filter(GuacamoleClientInfo.protocol == protocol).first()
        guacamole_client=None
        if result != None:
            result.user_info = client_id
            result.image = image
            result.status = 1
            result.latest_active_timestamp = str(datetime.now())
            guacamole_server = result.guacamole_server
            guacamole_client_name = result.guacamole_client_name
            guacamole_client_host = result.guacamole_client_host
            guacamole_client_vm = result.guacamole_client_vm
            protocol = result.protocol
            guacamole_client = guacamole_server+'client.xhtml?id=c/'+guacamole_client_name
            session.commit()
            
            # update GuacamoleServerLoad
            query = session.query(GuacamoleServerLoad)
            result = query.filter(GuacamoleServerLoad.guacamole_server == guacamole_server).first()
            result = self.__server_protocol_update(protocol, 1 , result)
            session.commit()
        session.close()
        self.lock.release()
        
        #TODO(): Need to start the corresponding container on the client_host with two parameters: guacamole_client_vm, image 
        return guacamole_client
    
    '''
        When creating a new guacamole server, there should be a config file there, or maybe just generated automatically
        But does it need to be a method in the class RestServer?
    '''
    def create_guacamole_server(self,client_id,image,protocal):
        self.lock2.acquire()
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.image == '').filter(GuacamoleClientInfo.protocol==protocal).first()#there is idle guacamole client
        if result != None:
            self.lock2.release()
            session.close()
            return
        else:
            session.close()
            
            #TODO(): new a Guacamole Server, config file name should be specified
            guacamoleserver.read_config('/home/kehl/workspace/OSSLab/conf/guacamole_server.xml')
        self.lock2.release()
        return None
        
    def remove_guacamole_server(self, guacamole_server):
        pass                      

if __name__ == '__main__':
    pass
