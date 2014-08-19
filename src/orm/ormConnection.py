from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tables import Guacamole

class ORMConnection:
    __DB_CONNECT_STRING = 'mysql+mysqldb://root:552523@localhost/kangjihua?charset=utf8'
    def __init__(self,username=None,password=None,server=None,database=None):
        if username!=None and password!=None and server!=None and database!=None: 
            self.__DB_CONNECT_STRING = 'mysql+mysqldb://'+username+':'+password+'@'+server+'/'+database+'?charset=utf8'
        self.__engine = create_engine(self.__DB_CONNECT_STRING, echo=False)
        self.__DB_Session = sessionmaker(bind=self.__engine)
        self.__session = self.__DB_Session()
    def getSession(self):
        return self.__session

def activate(user_lab_id):
    orm = ORMConnection()
    session = orm.getSession()
    query=session.query(Guacamole)
    temp = query.filter(Guacamole.user_info==user_lab_id).first()
    if temp==None:
        return
    if temp.status_info==0:
        temp.status_info = 1
    temp.latest_active_timestamp = datetime.now()
    session.commit()

def shutdown(user_lab_id):
    orm = ORMConnection()
    session = orm.getSession()
    query=session.query(Guacamole)
    temp = query.filter(Guacamole.user_info==user_lab_id).first()
    if temp==None:
        return
    temp.status_info = 0
    session.commit()

def addConnection(user_lab,guacamole_url):
    orm = ORMConnection()
    session = orm.getSession()
    temp = Guacamole(user_lab,guacamole_url,datetime.now(),True)
    session.add(temp)
    session.commit()

def findConnection(user_lab):
    orm = ORMConnection()
    session = orm.getSession()
    query=session.query(Guacamole)
    temp = query.filter(Guacamole.user_info==user_lab).first()
    if temp!=None:
        return temp.session_info
    return None

def delConnection(user_lab):
    orm = ORMConnection()
    session = orm.getSession()
    query=session.query(Guacamole)
    temp = query.filter(Guacamole.user_info==user_lab).first()
    if temp!=None:
        session.delete(temp)
        session.commit()

#============================test====================
def test_activate():
    activate('kangjihua_python')
def test_shutdown():
    shutdown('kangjihua_python')


if __name__=='__main__':
    test_activate()
    test_shutdown()