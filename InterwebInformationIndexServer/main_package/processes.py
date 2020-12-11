#handles all multiprocessed classes - Servers and stuff

from main_package.network import SocketServer
from main_package.network import ConnectionHandler
from main_package.services import ServiceHandler
from main_package.ftp import FTPService

import multiprocessing
import time

class ProcessHandler:

    socket_server = multiprocessing.Process(target=SocketServer.main)
    connection_handler = multiprocessing.Process(target=ConnectionHandler.main)
    service_handler = multiprocessing.Process(target=ServiceHandler.main)
    ftp_server = multiprocessing.Process(target=FTPService.main)

    processes = []
    inactive_processes = []
    shutdown = False;

    @staticmethod
    def main():
        
        ProcessHandler.inactive_processes = [ProcessHandler.socket_server, ProcessHandler.connection_handler, ProcessHandler.service_handler, ProcessHandler.ftp_server]

        for process in ProcessHandler.inactive_processes:
            print(process)

            if (ProcessHandler.start_process(process)):
                ProcessHandler.proccess.add(process)
                ProcessHandler.inactive_processes.remove(process)
            else:
                print('[ERROR] Process ' + str(process) + ' failed to start!')

        if (len(ProcessHandler.inactive_processes)):
            print('[WARN] iii process(es) failed to start! iii functionality may be diminished or this may lead to a crash!')
        else:
            print('[OK] All sub processes successfully started!')

        start = time.time()

        while (ProcessHandler.shutdown != True):
            time_elapsed = time.time() - start

            if time_elapsed % 5:
                for process in ProcessHandler.processes:

                    if (not process.is_alive()):

                        print['[ERROR] Process ' + str(process) + ' has stopped! Attempting to restart...']

                        print('[INFO] Process restart status: ' + str(ProcessHandler.restart_process(process)))

        #shutdown
        ProcessHandler.shutdown()


    @staticmethod
    def start_process(process):
        process.start()
        time.sleep(5) #wait 5 seconds for process to spawns
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

