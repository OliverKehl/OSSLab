#coding=utf-8
import restserver,unittest
class RestServerTest(unittest.TestCase):
    def setUp(self):
        self.restserver = restserver.RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml','/home/kehl/authentication.xml')
    def test_get_virtual_machine(self):
        #rs = restserver.RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml','/home/kehl/authentication.xml')
        host = self.restserver.get_guacamole('kangjihua', 'python')
        print host
if __name__=='__main__':
    unittest.main()
        
    
        