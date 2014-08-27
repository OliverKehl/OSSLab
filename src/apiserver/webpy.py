#coding=utf-8
import web,json,restserver
import ormConnection
urls = ('/(.*)', 'index')
#init the ORM Session
ormConnection.init_session()

#Rest Server

class index:
    def __init__(self):
        pass
        
    def parse(self,uri):
        pass

    def GET(self,info):
        web.input(info=None)
        #shit=web.ctx.items()
        #print shit
        info = str(info)
        info = info.split('_')
        print info
        client=''
        if info[0]=='1':#ask for a guacamole server
            client = restserver.get_guacamole_client(info[1],info[2],info[3])           
        elif info[0]=='2':#heart beat
            restserver.heart_beat(info[1],info[2])
        elif info[0]=='3':#reset guacamole client
            restserver.reset_guacamole_client(info[1], info[2])
        '''
        if result==1:
            pyDict = rs.get_virtual_machine_by_lab(info[1])
            web.header('Content-Type', 'application/json')
            return json.dumps(pyDict)
        elif result==2:
            pass
        elif result==3:
            pass
        elif result==4:
            return rs.fuck
        else:
            return 'Illegal Request'
        '''
        return client

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()