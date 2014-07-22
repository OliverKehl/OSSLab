#coding=utf-8
import azureservice,constants,unittest

class TestAzureService(unittest.TestCase):
    def setUp(self):
        self.azureservice = azureservice.AzureService(constants.SUBSCRIPTION_ID,constants.CERT_FILE)
        