import restserver,unittest
class RestServerTest(unittest.TestCase):
    def setUp(self):
        self.restserver = restserver.RestServer('/home/kehl/workspace/OSSLab/conf/lab_vm.xml')
    def test_get_virtual_machine(self):
        vm = self.restserver.get_virtual_machine('python')
        self.assertIsNotNone(vm)
        self.assertIsNotNone(vm['lab'])
        self.assertIsNotNone(vm['hostname'])
        self.assertIsNotNone(vm['username'])
        self.assertIsNotNone(vm['password'])
        self.assertIsNotNone(vm['port'])
        self.assertEqual(vm['lab'],'python')
if __name__=='__main__':
    unittest.main()
        
    
        