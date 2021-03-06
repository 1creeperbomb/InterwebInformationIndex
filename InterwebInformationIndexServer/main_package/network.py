#contains socket server and handles connections

import socket
import socketserver
from main_package.xml import XMLIndex
import urllib.request

class SocketServer:
    port = 5001 #default is 5001
    localhost = '127.0.0.1'

    def main():

        try:

            with socketserver.TCPServer(('', SocketServer.port), SocketHandler) as server:
                SocketServer.state = True
                print('[OK] Succesfully started network process!')
                server.serve_forever()

        except:
            print('[ERROR] Failed to start socket server! Port is already in use! (check if III is already running or if another program is using port ' + str(SocketServer.port) + ')')

class SocketHandler(socketserver.StreamRequestHandler):

    def handle(self):
        self.data_raw = self.rfile.readline().strip()
        print('data sent: ')
        print(self.data_raw)
        print('address: ')
        print(format(self.client_address[0]))

        #convert bytes to str
        self.data = self.data_raw.decode('utf8')
        type = XMLIndex.get_xml_type(self.data)

        if(type == None):
            print('unusable data, ending connection')
            return
        elif(type == 'master' or type == 'peer'):
            XMLIndex.parse_xml_string(self.data)
        elif(type == 'sync'):
            #return contents of index data
            sync_data = XMLIndex.get_data(xpath='/root/*',tree = et.parse('index.xml', parser))

            client_connect = SocketClient()

            for child in sync_data:
                raw_data = et.tostring(child).decode('utf8')
                client_connect.send_data(raw_data)

            self.request.sendall(b'<received/>')

        elif(type == 'request'):
            #send requested data
            pass
        elif(type == 'uaddress_location'):
            #return dir of service requested (for ftp)
            pass

class SocketClient:
    port = 5001
    IP = '127.0.0.1'
    socket_type = socket.AF_INET

    def __init__(self, IP=None, port=None):

        if IP != None:
            self.IP = IP
        if port != None:
            self.port = port

        is_v4 = SocketClient.is_valid_ipv4_address(IP)
        is_v6 = SocketClient.is_valid_ipv6_address(IP)

        if is_v4 == True:
            self.socket_type = socket.AF_INET
        elif is_v6 == True:
             self.socket_type = socket.AF_INET6

    def send_data(self, data):
        data_raw = data.encode('utf8')

        with socket.socket(self.socket_type, socket.SOCK_STREAM) as sock:

            try:
                sock.connect((self.IP, self.port))
                sock.sendall(data_raw)
                return_data = sock.recv()
            except:
                print('Failed to send data')
                return False

        return_data = return_data.decode('utf8')
        type = XMLIndex.get_xml_type(return_data)

        if type == None:
            print('Unsuable/corupt data')
            return False
        elif type == 'received':
            return True
        elif type == 'version':
            pass

        sock.close()
        return True

    @staticmethod
    def is_valid_ipv4_address(address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False

        return True

    @staticmethod
    def is_valid_ipv6_address(address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True
    
    @staticmethod
    def get_public_ip():

        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8') #update this in the future with a decentral solution?
        return external_ip

class ConnectionHandler:

    connections = []
    peer_max = 16 #maximum peers to stay active with

    @staticmethod
    def main():
        
        #debug loopback connection
        localhost = SocketClient('127.0.0.1', 5001)
        ConnectionHandler.connections.append(localhost)

        #while True:

            # If peers are less than peer_max, read from peer service to add a peer (based on location)
            #pass
    
    @staticmethod
    def send_data(data):

        for client in ConnectionHandler.connections:
            client.send_data(data)


        


#old stuff for reference using socket
'''
class SocketServerAccepter:
    #global vars

    port = 5000 #default is 5000
    host = '127.0.0.1'

    @staticmethod
    def main():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind(('', 80))

        s.listen(5)

        print('server is now listening for connections!')

        while True:

            c, addr = s.accept()
            print(addr)

            #add to handler list
            SocketServerHandler.add_connection(c, 'server')


class SocketServerHandler:

    server_connections = []
    client_connections = []

    @staticmethod
    def add_connection(socket, type):
        if type == 'server':
            server_connections.append(socket)
        elif type == 'client':
            client_connections.append(socket)

class SocketConnection:

    def __init__(self):
        pass

'''
        