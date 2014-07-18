from azure import (
    WindowsAzureError,
    MANAGEMENT_HOST,
    _validate_not_none,
    )
from azure.servicemanagement import *
from constants import *
import RestServer



class AzureService():
    def __init__(self, subscription_id=None, cert_file=None, host=MANAGEMENT_HOST):  # 'management.core.chinacloudapi.cn'
        '''
        constructor
        '''
        self.sms = ServiceManagementService(SUBSCRIPTION_ID, CERT_FILE)
        self.connected = True
    
    def create_storage(self, storage_name):
        self.sms.create_storage_account(storage_name, label=storage_name, location=LOCATION)
    
    def check_hosted_service_exist(self, hosted_service_name):
        hosted_services = self.sms.list_hosted_services()
        for service in hosted_services:
            if hosted_service_name == service.service_name:
                return True
        return False
    
    def _linux_config(self,hostname):
        linux_config = LinuxConfigurationSet(hostname,'opentech','@dministrat0r',True)
        linux_config.disable_ssh_password_authentication=False
        return linux_config
    
    
    def _os_hd(self,image_name,target_container_name,target_blob_name):
        media_link = ''
        os_hd= OSVirtualHardDisk(image_name,media_link)
        return os_hd
    
    def _network_config(self):
        network_config = ConfigurationSet()
        network_config.configuration_set_type='NetworkConfiguration'
        network_config.input_endpoints.input_endpoints.append(
                    ConfigurationSetInputEndpoint('ssh','tcp','22','22'),
                    ConfigurationSetInputEndpoint('vnc','tcp','5900','5900'),
                    ConfigurationSetInputEndpoint('http','tcp','80','80'),
                    ConfigurationSetInputEndpoint('http2','tcp','8080','8080'),
                    ConfigurationSetInputEndpoint('rdp','tcp','3389','3389'),
                    ConfigurationSetInputEndpoint('https','tcp','443','443'),
                    )
        return network_config
    
    def create_linux_vm(self, hosted_service_name, deployment_name):
        hosted_service_exist = self.check_hosted_service_exist(hosted_service_name)
        if hosted_service_exist == False:
            self.sms.create_hosted_service(service_name=hosted_service_name, label=hosted_service_name, description=None,
                                           location=LOCATION, affinity_group=None, extended_properties=None);
            
        linux_config = self._linux_config(deployment_name)
        os_hd = self._os_hd(LINUX_IMAGE, target_container_name, target_blob_name)
        network_config = self._network_config()
        self.sms.create_virtual_machine_deployment(hosted_service_name, deployment_name, deployment_slot='production', label=deployment_name,
                                                   role_name=deployment_name, linux_config, os_hd, network_config, 
                                                   availability_set_name=None, data_virtual_hard_disks=None,
                                                   role_size=None, role_type='PersistentVMRole', virtual_network_name=None)
    
    def create_windows_vm(self, hosted_service_name, deployment):
        pass
    