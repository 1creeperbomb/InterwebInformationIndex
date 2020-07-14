#debug file to test classes and import
from main_package.cryptographer import Cryptographer
from main_package.xml import XMLIndex
from main_package.network import SocketServer
from main_package.network import SocketClient

import multiprocessing

import socket

from lxml import etree as et



#Cryptographer.generate_keypair('ctpQ7pyNmqMPer9aVkAf8YSe')

print(SocketClient.get_public_ip())



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

