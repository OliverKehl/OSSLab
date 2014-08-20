#coding=utf-8
import paramiko,datetime,thread
from xml.etree.ElementTree import ElementTree
from ormConnection import ORMConnection
from tables import GuacamoleClientInfo
from MySQLdb import DATETIME
'''
@author: kehl
@contact: t-jikang@microsoft.com
@version: 0.0

First version with guacamole_server information stored in memory but not in database
'''

class RestServer():
    guacamole_servers=[]
    lock = thread.allocate_lock()
    lock2 = thread.allocate_lock()
    def __init__(self):
        pass
    
    def get_guacamole_client(self,client_id,lab_name):
        session = ORMConnection().getSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == client_id).filter(GuacamoleClientInfo.lab == lab_name).first()
        if result!=None:
            if result.status==0:
                result.status = 1
            result.latest_active_timestamp = datetime.datetime().now()
            session.commit()
            return result.guacamole_client
        else:
            res = self.establish_guacamole_client(client_id,lab_name)
            if res!=None:
                return res
            
            #need to new a guacamole server
            self.create_guacamole_server(client_id, lab_name)
            return self.get_guacamole_client(client_id, lab_name)
    
    '''
        When creating a new guacamole server, there should be a config file there, or maybe just generated automatically
    '''    
    def create_guacamole_server(self,client_id,lab_name):
        self.lock2.acquire()
        session = ORMConnection().getSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == client_id).filter(GuacamoleClientInfo.lab == lab_name).first()
        if result!=None:
            self.lock2.release()
            return
        
        
        #new a Guacamole Server
        
        self.lock2.release()
        return None
        
                          
    
    def establish_guacamole_client(self,client_id,lab_name):
        self.lock.acquire()
        session = ORMConnection().getSession()
        query = session.query(GuacamoleClientInfo) 
        result = query.filter(GuacamoleClientInfo.user_info == '').filter(GuacamoleClientInfo.lab == lab_name).first()
        res = None
        if result!=None:
            result.user_info = client_id
            result.status = 1
            result.latest_active_timestamp = datetime.datetime.now()
            res = result.guacamole_client
            session.commit()
        self.lock.release()
        return res
            
    
if __name__=='__main__':
    pass