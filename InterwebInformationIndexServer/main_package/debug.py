#debug file to test classes and import
from main_package.cryptographer import Cryptographer
from main_package.xml import XMLIndex, XMLServiceDefinition, XMLService
from main_package.network import SocketServer
from main_package.network import SocketClient
from main_package.services import Service
from main_package.network import ConnectionHandler
from main_package.ftp import FTPService

import multiprocessing

import socket

from lxml import etree as et

import subprocess
import os, signal
from os import system, name as os_name
import time
import glob





XMLService.generate_new_definition('lol', 'lol', 'debug/mysite', 'all', 'WzJmdiSCSxk5dnT6P65UhDyNdjBnBy5E3fDxigWOHCs=')















#test = FTPService()

#test.main()


'''

buffer = []

test_process = subprocess.Popen(['C:/Users/ismae/Desktop/lolz.pub/iiistart.bat'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#outs, errs = test_process.communicate()

#print(outs.decode('utf8'))
while True:
    print(test_process.poll())
    line = test_process.stdout.readline().decode('utf8')
    print(line)
    buffer.append(line)

    if test_process.poll() == 0:
        print('YEAHHHHHHHH')

    if len(buffer) > 100:
        buffer.pop(0)
        test = input('Enter data:').encode('utf8')
        test_process.stdin.write(test)
        


print(test_process.poll())


'''





#XMLServiceDefinition.get_service_files('service1')

#print(XMLIndex.get_data('/root/master[address[text()="WzJmdiSCSxk5dnT6P65UhDyNdjBnBy5E3fDxigWOHCs="]]/services/service[desc[@name = "woot"]]/@version')[0])

#print(os.path.relpath('C:\\Users\\ismae\\Desktop\\lolz.pub'))

#test = XMLServiceDefinition.get_service_files('services/service.1')

#for thing in test:
 #   print(thing)

#xml = input('XML: ')

#ConnectionHandler.main()
#ConnectionHandler.send_data(xml)

xml = '''<master iiiVersion="1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <address>12URI46pikzI54c9xqvaW47IZ/SLxD8pNSXk4t/+a0Y=</address>
    <sign salt="TB8UP9FU8K904BQ0">T631m658ZXg7fHneyVqBJTZ9qP0PrcCHo0Z4qAukpRKF4DIo+EXUV7gF3oFlw7kQMS3VP7CqeRTw04XN2LiVBA==</sign>
    <desc name="lolzzzzzz">yeeee</desc>
    <services>
      <service version="XPt5QZbvqZOV87a0FginOrumyhOAFsJAWNxrFpC+REE=" counter="2">
        <desc name="lolz">pub</desc>
        <data>
          <files>
            <file rdir="assets" type="static">0</file>
            <file rdir="example.txt" type="static">AniFF4QEUV8v1/swgxj2pD7/gQr/5bEwLvkledBvE8c=</file>
            <file rdir="iiistart.bat" type="static">AniFF4QEUV8v1/swgxj2pD7/gQr/5bEwLvkledBvE8c=</file>
            <file rdir="index.html" type="static">3UEMMYL31Zf9RMMxcPTcJlOExOvJZ1OsmKsG9YnNJ+Q=</file>
            <file rdir="lol" type="variable">0</file>
            <file rdir="test.xml" type="variable">0</file>
            <file rdir="yeet.txt" type="static">lMWbJZM5FzgGgIVLsq0YV/CpQsJYFCeLl0AWcLVICyU=</file>
            <file rdir="assets/urmum.txt" type="static">DldRwCblQ7Loqy6wYJnaodHl30d3j3eH+qtFzfEv46g=</file>
          </files>
        </data>
        <tags>
            <DELETE/>
        </tags>
      </service>
    </services>
  </master> '''

#XMLIndex.parse_xml_string(xml)


'''
#uaddress = XMLIndex.get_data('peer/services')

#XMLServiceDefinition.verify_service('WzJmdiSCSxk5dnT6P65UhDyNdjBnBy5E3fDxigWOHCs=','woot')

#files = glob.glob('services/service1/**/*', recursive=True)

for file in files:
    print(file)
    print('_________________')
    print('MODIFIED:')
    test = os.path.relpath(os.path.realpath(file))
    test.replace('\\', '/')
    print(test)
    print('_________________')
'''



'''
with open('services/service1/.iii/uaddress.txt', 'r') as uaddress_file:
            uaddress_text = uaddress_file.read()
            uaddress_split = uaddress_text.split('.', 1)
            print(uaddress_split)
'''

'''
filename = os.path.abspath('services/service1/iiistart.bat')

process = subprocess.Popen([filename], creationflags=subprocess.CREATE_NEW_CONSOLE)

#stdout=subprocess.DEVNULL
#stdin=PIPE, stderr=PIPE, stdout=PIPE,

time.sleep(2)
print ('proc1 = ' + str(process.pid))

print('test')

process.kill()

print ('proc1 = ' + str(process.pid))
'''

'''
#Cryptographer.generate_keypair('ctpQ7pyNmqMPer9aVkAf8YSe')

#print(SocketClient.get_public_ip())
key = Cryptographer.read_key('1234')
crypto = Cryptographer(key, False)
address = crypto.get_public_key()

print(address)

print(XMLIndex.get_data('master', address))

#print(XMLIndex.modify_node('master', address, 'NEW NAME'))
'''

'''
#XMLIndex.parse_xml_string()

#+R+zzu0IiLjR1mliwAcxTHVoWT9pzMC5ptw=

crypto = Cryptographer('lxQZfMmb+R+zzu0IiLjR1mliwAcxTHVoWT9pzMC5ptw=', False)

print(crypto.private_key)
print(crypto.public_key)
'''


'''
data = XMLIndex.get_data(xpath='/root/*',address=None,tree=None)

print(data)

for child in data:
    print(et.tostring(child).decode('utf8'))
'''

'''
if __name__ == '__main__': #this must be the main method in the main class so that it can handle the processes in a list

    process = multiprocessing.Process(target=SocketServer.main)
    process.start()
    process.terminate()

    #send test data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 5001))
        sock.sendall(b'<fardpant/>')

 ''' 

'''
#Cryptographer.generate_keypair('test password')
private_key = Cryptographer.read_key('test password')

crypto = Cryptographer(private_key, False)

print('private key: ' + private_key)

data_test = '<services><service version="+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs="><desc name="woot">ya man</desc><data><files><file rdir="assets/pic.img" type="static">+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs=</file></files></data></service></services>'
signed = crypto.sign_data(data_test)

print(signed)

verified = crypto.verify_data(data_test, signed)

print(verified)

#print(Xml_index.get_data('4O5y6PUBZD6Kziz2eWo3n1TNHVTfT7x6eKwLPPUdVls=', 'peer'))

XMLIndex.parse_xml_string('<master><address>WzJmdiSCSxk5dnT6P65UhDyNdjBnBy5E3fDxigWOHCs=</address><sign salt="1234567890123456">ptNtqdUn/MtpoHFLgcodcYaD9DAmV3xVRI9+/K7pZGYIccNd61KC4LrIZz+bEhznR+f3p/hXWK7jWD/jzPdXCw==</sign><desc name="my master node">my EVEN cool master node</desc><services><service version="+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs="><desc name="woot">ya man</desc><data><files><file rdir="assets/pic.img" type="static">+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs=</file></files></data></service></services></master>')

#<services><service version="+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs="><desc name="woot">ya man</desc><data><files><file rdir="assets/pic.img" type="static">+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs=</file></files></data></service></services>
'''

