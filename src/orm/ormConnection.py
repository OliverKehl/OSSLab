from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from tables import Guacamole

class ORMConnection:
    __DB_CONNECT_STRING = 'mysql+mysqldb://root:552523@localhost/kangjihua?charset=utf8'
    def __init__(self,username=None,password=None,server=None,database=None):
        if username!=None and password!=None and server!=None and database!=None: 
            self.__DB_CONNECT_STRING = 'mysql+mysqldb://'+username+':'+password+'@'+server+'/'+database+'?charset=utf8'
        self.__engine = create_engine(self.__DB_CONNECT_STRING, echo=True)
        self.__DB_Session = sessionmaker(bind=self.__engine)
        self.__session = self.__DB_Session()
    def getSession(self):
        return self.__session



orm = ORMConnection()
session = orm.getSession()
#init_db()    
#g1 = Guacamole('kangjihua_python','osslab.chinacloudapp.cn:8080/guacamole/ssh',datetime.now(),False)
#g1 = session.query(Guacamole).filter(Guacamole.user_info.in_(['kangjihua_python'])).all()[0]
query=session.query(Guacamole)
g1 = query.filter(Guacamole.user_info=='kangjihua_python').first()
print g1
#session.commit()


