from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
Base = declarative_base()
#Table
class Guacamole(Base):
    __tablename__='guacamole'
    
    id = Column(Integer,primary_key=True)
    user_info = Column(String(50))
    session_info=Column(String(50))
    latest_active_timestamp=Column(DateTime)
    status_info = Column(Boolean)
    
    def __init__(self,user_info,session_info,latest_active_timestamp,status_info):
        self.user_info = user_info
        self.session_info = session_info
        self.latest_active_timestamp = latest_active_timestamp
        self.status_info = status_info
        
    def __repr__(self):
        return "<Guacamole('%s','%s','%s','%s')>" % (self.user_info,self.session_info,str(self.latest_active_timestamp),self.status_info)

if __name__=='__main__':
    engine = create_engine('', echo=True)#DB path
    Base.metadata.create_all(engine)
    