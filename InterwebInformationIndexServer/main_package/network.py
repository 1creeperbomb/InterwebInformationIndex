#contains socket server and handles connections

import socket
import socketserver
from main_package.xml import XMLIndex

class SocketServer:
    port = 5001 #default is 5001
    localhost = '127.0.0.1'

    def main():

        try:

            with socketserver.TCPServer(('', SocketServer.port), SocketHandler) as server:
                SocketServer.state = True
                print('Succesfully started network process!')
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

class SocketClient:
    port = 5001
    IP = '127.0.0.1'

    def __init__(self, IP, port):

        if IP != None:
            self.IP = IP
        if port != None:
            self.port = port

    def send_data(self, data):
        data_raw = data.encode('utf8')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

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
        