'''
@author: kehl
@contact: t-jikang@microsoft.com
'''

import thread
from xml.etree.ElementTree import ElementTree
from ormConnection import ORMConnection
from tables import GuacamoleClientInfo,GuacamoleServerLoad
from datetime import datetime
    
def read_config(config_file):
    session = ORMConnection().getSession()
    tree = ElementTree()
    tree.parse(config_file)
    root = tree.getroot()
    server = root.attrib['name']
    labs = root.getchildren()
    cnt = 0
    for lab in labs:
        cnt+=1
        labname = lab.attrib['name']
        guacname = lab[0].text
        #user_info='',guacamole_server='',guacamole_client='',lab='',status=0,latest_active_timestamp=''
        guacamoleClientInfo = GuacamoleClientInfo('',server,server+'client.xhtml?id=c/'+guacname,labname,0,datetime.now())
        session.add(guacamoleClientInfo)
    session.commit()
    session.add(GuacamoleServerLoad(server,cnt))
    session.commit()
        

if __name__=='__main__':
    read_config('/home/kehl/workspace/OSSLab/conf/guacamole_server.xml')
    