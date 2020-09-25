from ftplib import FTP
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import os
import logging

#handles all file transfer stuff

#consider using multithreaded or multiprocess server based on speed

class FTPService:

    port = 5002 #default is 5002
    read_limit = 52428800 #50 mbps
    write_limit = 52428800
    
    def main(self):
        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # anonymous user
        authorizer.add_anonymous('services')

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        # Define a customized banner (string returned when client connects)
        handler.banner = "iii ftp server ready."

        dtp_handler = ThrottledDTPHandler
        dtp_handler.read_limit = self.read_limit  # 30 Kb/sec (30 * 1024)
        dtp_handler.write_limit = self.write_limit  # 30 Kb/sec (30 * 1024)

        handler.dtp_handler = dtp_handler

        # Specify a masquerade address and the range of ports to use for
        # passive connections.  Decomment in case you're behind a NAT.
        #handler.masquerade_address = '151.25.42.11'
        #handler.passive_ports = range(60000, 65535)

        # Instantiate FTP server class and listen on 0.0.0.0:2121
        address = ('127.0.0.1', self.port) #local address is debug, change to epmty and enable masquerade settings later

        try:
            server = FTPServer(address, handler)
        except:
            print('[WARN] FTP Service failed to start. Port ' + str(self.port) + ' for iii FTP server is already in use!')
            return

        logging.basicConfig(filename='iii_logs/ftp.log', level=logging.INFO)

        # set a limit for connections
        server.max_cons = 256
        server.max_cons_per_ip = 5

        # start ftp server
        server.serve_forever()

class FTP:
    pass
