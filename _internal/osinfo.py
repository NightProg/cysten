import sys
import os



def get_os_info():
    if sys.platform == 'win32':
        return 'Windows'
    elif sys.platform == 'darwin':
        return 'Mac OS X'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    else:
        return 'Unknown'
    

def get_os_version():
    if sys.platform == 'win32':
        return sys.getwindowsversion().version
    elif sys.platform == 'darwin':
        return '.'.join(map(str, os.uname()[2].split('.')[:2]))
    elif sys.platform.startswith('linux'):
        return ' '.join(os.uname()[:3])
    else:
        return 'Unknown'

def get_c_default_compiler():
    if sys.platform == 'win32':
        return 'cl'
    else:
        return 'gcc'

def get_cpp_default_compiler():
    if sys.platform == 'win32':
        return 'cl'
    else:
        return 'g++'