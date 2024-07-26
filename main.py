import argparse
import os
import sys
import subprocess
from mitmproxy import Proxy
import concurrent.futures

def list_devices():
    pid = subprocess.Popen(['adb', 'devices'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    pid.wait()
    results = pid.communicate()[0].strip()
    devices = results.split(b'\n')[1:]
    list_emu = []
    result = []

    for device in devices:
        name, state = device.split(b'\t')
        result.append(name.decode('utf8'))
    
    return result

def map_deviceids(device_id):
    mapping = {}
    all_devices = list_devices()
    
    for deviceId in all_devices:
        if(device_id == deviceId):
            mapping[device_id] = deviceId
        else:
            pid = subprocess.Popen(['adb', '-s', deviceId, 'emu', 'avd', 'name'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid.wait()
            data = pid.communicate()[0].strip()
            emu_name = data.decode('utf-8').split('\n')[0].strip()
            mapping[emu_name] = deviceId

    return mapping

def check_is_it_up(deviceId):
    pid = subprocess.Popen(['adb', '-s', deviceId, 'shell', 'getprop', 'dev.bootcomplete'], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    pid.wait()
    return b'1' in pid.communicate()[0]

def check_device_status(device_id):
    mapping = map_deviceids(device_id)
    if(device_id in mapping):
        while True:
            if(check_is_it_up(mapping[device_id])):
                print('Device is UP!')
                return True
            else:
                print('Waiting for the device to be in running state!')
                sys.exit(-1)

def main():
    parser = argparse.ArgumentParser(description="Running the mitmproxy capture the traffic.....")
    parser.add_argument("-pkg", "--package_name", help="Package to intercept the traffic", type=str)
    parser.add_argument("-cap", "--capture", help="Capture all the traffic")
    parser.add_argument("-id", '--device_id', help="Enter the device ID", type=str, required=True)
    parser.add_argument("-t", "--timeout", help="Number of seconds the script will run to capture all the traffic.", type=int, default=300)
    parser.add_argument("-p", "--port", help="Specify the port number on the proxy is set to get the intercepted traffic", type=int)
    parser.add_argument("-i", "--inject", help="Pass the CA certificate path to be injected to the system trusted CA certicates in the emulator", type=str)
    parser.add_argument("-c", "--clear", help="Remove all the previous apps network traffic")
    parser.add_argument("-cert", "--rename_cert", help="Rename the mitmproxy or burp suite certificate.", type=str)
    args = parser.parse_args()
    
    if(args.rename_cert and os.path.isfile(args.rename_cert)):
        cwd = os.getcwd()
        script_path = os.path.join(cwd, 'rename_ca_cert.sh')
        subprocess.run(['chmod', '+x', script_path])
        subprocess.run([script_path, args.rename_cert])

    if(args.inject and os.path.isfile(args.inject)):
        if(args.device_id and check_device_status(args.device_id)):
            print('Started inject the script')
            certificate_path = os.path.join('/sdcard/Download', os.path.basename(args.inject))
            if(os.path.isfile(args.inject)):
                inject_cert_script = os.path.join(os.getcwd(), 'inject_certificate.sh')
                subprocess.run(['adb', 'push', args.inject, '/sdcard/Download'])
                subprocess.run(['adb', 'push', inject_cert_script, '/data/local/tmp'])
                subprocess.run(['adb', 'shell', 'su', '-c', 'setprop', 'CERTIFICATE_PATH', certificate_path])
                subprocess.run(['adb',  'shell', 'su', '-c', 'chmod', '+x', '/data/local/tmp/inject_certificate.sh'])
                subprocess.run(['adb', 'shell', 'su', '-c', '/data/local/tmp/inject_certificate.sh', certificate_path])
                print('Successfully injected the mitmproxy certicate with the system trusted CA certificate')

    if(args.capture):
        if(args.package_name and args.port):
            proxy = Proxy(args.package_name, args.port, args.timeout)
            if(args.clear):
                proxy.empty_httptools()
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                t1 = executor.submit(proxy.httptool_proxy)
                t2 = executor.submit(proxy.mitmdump)
                try:
                    concurrent.futures.wait([t1, t2])
                except KeyboardInterrupt:
                    print("Program interrupted!")
                    sys.exit(-1)
        else:
            print('Please enter the package number or port to capture the traffic!!')
            sys.exit(-1)
        
        
if __name__ == "__main__":
    main()
    
