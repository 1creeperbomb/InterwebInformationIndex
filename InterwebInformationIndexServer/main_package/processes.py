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
        #connection_handler = multiprocessing.Process(target=ConnectionHandler.main)
        #service_handler = multiprocessing.Process(target=ServiceHandler.main, args=(address,))
        ftp_server = multiprocessing.Process(target=FTPService.main)

        #global processes
        processes = [socket_server, ftp_server] #connection_handler, service_handler,
        shutdown = False

        for process in processes:
            ProcessHandler.start_process(process)

        while shutdown == False:
            time.sleep(10)
            print('status')
            for prco in processes:
                print(proc.is_alive)
            #print(socket_server.is_alive)
            #print(connection_handler.is_alive)
            #print(service_handler.is_alive)
            #print(ftp_server.is_alive)

        #shutdown
        ProcessHandler.shutdown()

    @staticmethod
    def get_status():
        for proc in processes:
            stat += proc + ' : ' + proc.is_alive
        return stat

    @staticmethod
    def start_process(process):
        process.start()
        time.sleep(3) #wait 3 seconds for process to spawns
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

