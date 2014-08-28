class StartContainerException(Exception):
    pass

def create_container(vm = '',port = -1,image=''):
    return False