from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
Base = declarative_base()

'''
    Used to record those guacamole clients
    Fields: id, guacamole_server, guacamole_client, lab, status, user_info(can be NULL), latest_active_timestamp
'''
class GuacamoleClientInfo(Base):
    __tablename__='guacamole_client_info'
    
    id = Column(Integer,primary_key=True)
    user_info = Column(String(50))#can be empty
    guacamole_server = Column(String(50))
    guacamole_client=Column(String(50))
    lab = Column(String(20))
    latest_active_timestamp=Column(DateTime)
    status = Column(Boolean)
    
    def __init__(self,user_info='',guacamole_server='',guacamole_client='',lab='',status=0,latest_active_timestamp=''):
        self.user_info = user_info
        self.guacamole_server = guacamole_server
        self.guacamole_client = guacamole_client
        self.lab = lab
        self.status = status
        self.latest_active_timestamp = latest_active_timestamp
    
    def __repr__(self):
        return "<GuacamoleClientInfo('%s','%s','%s','%s','%s','%s')>" %(self.user_info,
                                                                             self.guacamole_server,
                                                                             self.guacamole_client,
                                                                             self.lab,
                                                                             str(self.status),
                                                                             str(self.latest_active_timestamp)
                                                                             )

'''
    Used to count how many current occupied linking is exsiting
    If count is 0, then it means this guacamole_server can be removed and all the available guacamole_client based 
    on this server shall be removed too.
'''
class GuacamoleServerLoad(Base):
    __tablename__='guacamole_server_load'
    id=Column(Integer,primary_key=True)
    guacamole_server = Column(String(50))
    count = Column(Integer)
    
    def __init__(self,guacamole_server,count):
        self.guacamole_server = guacamole_server
        self.count = count
    
    def __repr__(self):
        return "<GuacamoleServerLoad('%s,'%s')>" %(self.guacamole_server,str(self.count))

if __name__=='__main__':
    engine = create_engine('mysql+mysqldb://root:552523@localhost/kangjihua?charset=utf8', echo=True)#DB path
    Base.metadata.create_all(engine)
    