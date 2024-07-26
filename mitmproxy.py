import os
import subprocess
import time
import shutil

class Proxy:
    def __init__(self, pkg_name, port, timeout=None):
        self.pkg_name=pkg_name
        self.port = port
        self.timeout = timeout
        #self.mitm_dir = '/home/poonia/Documents/androsand/com.android.chrome'

    def httptool_proxy(self):
        p = subprocess.Popen(['httptools', '-m', 'capture', '-p', str(self.port), '-n', self.pkg_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            print('httptools process started running!')
            outs, errs = p.communicate(timeout=self.timeout)
            while True:
                if(p.returncode is not None):
                    print('httptools process stopped running!')
                    break
        except Exception as err:
            print('Terminating the httptools process!')
            p.kill()
            outs, errs = p.communicate()
            print(err)
        
    def mitmdump(self):
        p = subprocess.Popen(['mitmdump', '-n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            print('mitmdump process started running!')
            outs, errs = p.communicate(timeout=self.timeout)
            while True:
                if(p.returncode is not None):
                    print('mitmdump process stopped running!')
                    break
        except Exception as err:
            print('Terminating the mitmdump process!')
            p.kill()
            outs, errs = p.communicate()
            print(err)

    def check_output(self):
        username = os.path.expanduser('~')
        file_path = os.path.join(username, '.httptools/flows')
        file_flow = os.path.join(file_path, self.pkg_name+'.flow')
        file_flow_txt = os.path.join(file_path, self.pkg_name+'.flow.txt')
        files = []
        if(os.path.isdir(file_path)):
            if(os.path.isfile(file_flow)):
                files.append(file_flow)
            if(os.path.isfile(file_flow_txt)):
                files.append(file_flow_txt)
        else:
            print('Not Found httptools directory!!')

        return files
        
    def empty_httptools(self):
        username = os.path.expanduser('~')
        dir_path = os.path.join(username, '.httptools/flows')
        if(os.path.isdir(dir_path)):
            # Remove package files from the mentioned path.

            file_flow = os.path.join(dir_path, self.pkg_name+'.flow')
            file_flow_txt = os.path.join(dir_path, self.pkg_name+'.flow.txt')
            if(os.path.isfile(file_flow)):
                os.remove(file_flow)
            if(os.path.isfile(file_flow_txt)):
                os.remove(file_flow_txt)
        else:
            print('No httptools directory!!')



