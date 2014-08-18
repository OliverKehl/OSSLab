from ormConnection import ORMConnection
from tables import Guacamole
from datetime import datetime

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


def test_activate():
    activate('kangjihua_python')
def test_shutdown():
    shutdown('kangjihua_python')

if __name__=='__main__':
    test_activate()
    test_shutdown()