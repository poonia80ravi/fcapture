# fcapture
Capture the network traffic to file in android

# Installation
Install the dependencies from the requirements.txt file.

pip3 install -r requirements.txt

# Rename Certificate 
First step to install the CA certificate to the system trusted CA certificate in android user have to rename the certificate.
In case of mitmproxy the certificate could be found at default location(~/.mitmproxy/). Pass the certificate path to the below mentioned command.

python3 main.py -cert $Certificate_path

The rename certificate would be generated in the same directory the user has input while running.

# Install the rename Certificate in Android device.
First the user need to install a module ConscryptTrustUserCerts(https://github.com/nccgroup/ConscryptTrustUserCerts) in the magisk and reboot the system.

To inject the certicate to connected android device it requires the file the rename certicate and device id. 
python3 main.py -id $Device_Id -i $(Rename_Certificate_Path)

To check the certificate is installed in system trusted CA certificate.
Security & privacy -> More security & privacy -> Encryption & credentials -> Trusted Credentials -> System

# To capture the traffic and write to a file.
It requires mitmproxy and httptools python library to be installed.
Set the manual proxy in the wifi connection so that the traffic should be passed through that proxy and port number.
To capture the network traffic of any app. Pass the app package name and port number where you have set the proxy.

python3 main.py -id $Device_id -cap -pkg $package_name -p $port_number

