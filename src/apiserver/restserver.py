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
    
    def heart_beat(self, client_id, image):
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == client_id).filter(GuacamoleClientInfo.image == image).first()
        if result != None:
            result.status = 1
            from __builtin__ import str
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
            res = result.guacamole_client
            session.commit()
            session.close()
            return res
        else:
            session.close()
            res = self.establish_guacamole_client(client_id, image)
            if res != None:
                return res
            
            # need to new a guacamole server
            self.create_guacamole_server(client_id, lab_name)
            return self.get_guacamole_client(client_id, lab_name)
    
    def reset_guacamole_client(self, client_id, lab_name):
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.lab == lab_name).first()
        if result == None:
            return
        guacamole_server = result.guacamole_server
        result.status = 0
        result.userinfo = ''
        session.commit()
    
    def establish_guacamole_client(self, client_id, image, client_type=None):
        self.lock.acquire()
        session = DBSession()
        query = session.query(GuacamoleClientInfo)
        '''
        if the image is sensitive with client_type, then I should specify the client_type by using a map
        
        client_type = 
        '''
        if client_type == None:
            result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.image == '').first()
        else:
            result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.image == '').filter(GuacamoleClientInfo.client_type == client_type).first()
        res = None
        if result != None:
            result.user_info = client_id
            result.image = image
            result.status = 1
            result.latest_active_timestamp = str(datetime.now())
            guacamole_server = result.guacamole_server
            guacamole_client_name = result.guacamole_client_name
            guacamole_client_host = result.guacamole_client_host
            session.commit()
            
            # update GuacamoleServerLoad
            query = session.query(GuacamoleServerLoad)
            result = query.filter(GuacamoleServerLoad.guacamole_server == guacamole_server).first()
            if client_type=='ssh':
                result.ssh_count -= 1
            elif client_type=='vnc':
                result.vnc_count -= 1
            elif client_type=='vnc-readonly':
                result.vnc_readonly_count -= 1
            else:
                result.rdp_count -= 1
            result.server_load -= 1
            session.commit()
        session.close()
        self.lock.release()
        
        #need to start the corresponding container on the client_host
        #parameter shall be 
        return guacamole_server+'client.xhtml?id=c/'+guacamole_client_name
    
    '''
        When creating a new guacamole server, there should be a config file there, or maybe just generated automatically
        But does it need to be a method in the class RestServer?
    '''
    def create_guacamole_server(self):
        self.lock2.acquire()
        session = DBSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.lab == '').first()#there is idle guacamole client
        if result != None:
            self.lock2.release()
            session.close()
            return
        else:
            session.close()
            # new a Guacamole Server, config file name should be specified
            guacamoleserver.read_config('/home/kehl/workspace/OSSLab/conf/guacamole_server.xml')
        self.lock2.release()
        return None
        
    def remove_guacamole_server(self, guacamole_server):
        pass                      

if __name__ == '__main__':
    pass
