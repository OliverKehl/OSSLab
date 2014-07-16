from azure import (
    WindowsAzureError,
    MANAGEMENT_HOST,
    _validate_not_none,
    )
from azure.servicemanagement import *
import RestServer

subscription_id = '0db41f26-7fe8-4402-a13b-9efc38d25f14'
cert_file = '/home/kehl/mycert.pem'
class AzureService():
    def __init__(self, subscription_id=None, cert_file=None, host=MANAGEMENT_HOST):  # 'management.core.chinacloudapi.cn'
        '''
        constructor
        '''
        self.sms = ServiceManagementService(subscription_id, cert_file)
        self.connected = True
    
    def create_storage(self, storage_name):
        pass
    
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
        media_link=
        os_hd=OSVirtualHardDisk(image_name,media_link)
            
    def create_linux_vm(self, hosted_service_name, deployment_name):
        hosted_service_exist = self.check_hosted_service_exist(hosted_service_name)
        if hosted_service_exist == False:
            self.sms.create_hosted_service(service_name=hosted_service_name, label=hosted_service_name, description=None, \
                                        location='China East', affinity_group=None, extended_properties=None);
            
        
        self.sms.create_virtual_machine_deployment(hosted_service_name, deployment_name, deployment_slot='production', label=deployment_name,\
                                                    role_name=deployment_name, system_config, os_virtual_hard_disk, network_config=None, \
                                                    availability_set_name=None, data_virtual_hard_disks=None,\
                                                     role_size=None, role_type='PersistentVMRole', virtual_network_name=None)
    
    def create_windows_vm(self, hosted_service_name, deployment):
        pass
