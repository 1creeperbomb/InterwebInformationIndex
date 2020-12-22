#handles all multiprocessed classes - Servers and stuff

from main_package.network import SocketServer
from main_package.network import ConnectionHandler
from main_package.services import ServiceHandler
from main_package.ftp import FTPService

import multiprocessing
import time

class ProcessHandler:

    @staticmethod
    def main(address):
        
        socket_server = multiprocessing.Process(target=SocketServer.main)
        #onnection_handler = multiprocessing.Process(target=ConnectionHandler.main)
        #service_handler = multiprocessing.Process(target=ServiceHandler.main, args=(address,))
        #ftp_server = multiprocessing.Process(target=FTPService.main)

        global processes
        processes = [socket_server,] #connection_handler, service_handler, ftp_server
        shutdown = False

        for process in processes:
            ProcessHandler.start_process(process)

        while shutdown == False:
            #time.sleep(10)
            print('status')
            print(len(processes))
            print(socket_server.is_alive)
            for process in processes:
                print(process + ' : ' + process.is_alive)
            

        #shutdown
        ProcessHandler.shutdown()


    @staticmethod
    def start_process(process):
        process.start()
        #time.sleep(5) #wait 5 seconds for process to spawns
        return process.is_alive()

    @staticmethod
    def stop_process(process):
        process.terminate()
        process.join()

    @staticmethod
    def restart_process(process):
        stop_process(process)
        return start_process(process)

    @staticmethod
    def shutdown():

        if ProcessHandler.processes == None:
            pass
        else:
            for process in ProcessHandler.processes:
                process.terminate()
                process.join()

