#handles all multiprocessed classes - Servers and stuff

from main_package.network import SocketServer
from main_package.network import ConnectionHandler
from main_package.ftp import FTPService

import multiprocessing
import time
import sys

class ProcessHandler:

    shutdown = False

    @staticmethod
    def main():
        socket_server = multiprocessing.Process(target=SocketServer.main, name='III-server', daemon=True)
        #connection_handler = multiprocessing.Process(target=ConnectionHandler.main)
        ftp_server = multiprocessing.Process(target=FTPService.main, name='III-ftp', daemon=True)

        global processes
        processes = [socket_server, ftp_server] #connection_handler

        for process in processes:
            ProcessHandler.start_process(process)

        while ProcessHandler.shutdown == False:
            time.sleep(10)  #debug
            print('status')
            for proc in processes:
                print(proc.is_alive)

        #shutdown
        ProcessHandler.shutdown_all()

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
    def shutdown_all():
        if processes == None:
            pass
        else:
            for process in processes:
                process.terminate()
                process.join()

class Processes:

    def __init__(self):
        socket_server = multiprocessing.Process(target=SocketServer.main, name='III-server')
        ftp_server = multiprocessing.Process(target=FTPService.main, name='III-ftp')


#start
if __name__ == '__main__':
    ProcessHandler.main()
