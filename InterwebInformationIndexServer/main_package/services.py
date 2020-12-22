#Contains everything to load, run, handle services and etc.
import os
from os import name as os_name
import subprocess
from main_package.xml import XMLService
from main_package.cryptographer import Cryptographer
from lxml import etree as et
import time

class ServiceHandler:

    @staticmethod
    def main(address):

        #global handler_status
        #handler_status = True
        global my_address
        my_address = address
        
        global services
        services = []

        global reusable_names
        reusable_names = []

        #init all services in folder
        ServiceHandler.load_all()

        #start all services
        for service in services:
            service.start_service()

        #poll for status every interval
        while True:
            for service in services:
                raw_status = service.process.poll()

                if (raw_status == 1):
                    name = service.name
                    uaddress = service.uaddress
                    print('[WARN] Service ' + name + ' at uaddress ' + uaddress + ' exited with code 1 (error), III will attempt to restart it')
                    service.restart_service()

                    time.sleep(5)
                    raw_status = service.process.poll()

                    if (raw_status == 1 or raw_status == 0):
                        print('[WARN] Service ' + name + ' at uaddress ' + uaddress + ' exited with code ' + raw_status + ' (error), III failed to restart it')
                    else:
                        print('[INFO] Service ' + name + ' at uaddress ' + uaddress + ' was successfully restarted')

                elif (raw_status == 0):
                    print('[INFO] Service ' + name + ' at uaddress ' + uaddress + ' exited with code 0 (normal), III will not restart it')

                time.sleep(15)
    
    @staticmethod
    def load_all():
        #initilize services from service folder
        services_dir = os.listdir('services')

        for service_dir in services_dir:
            if os.path.isdir(service_dir):
                rel_service_path = os.path.join('services', service_dir)


                #load service from definition

                definition = XMLService.load_definition(rel_service_path)

                if defnition == False:
                    print('[WARN] The service located at ' + service_dir + ' failed to load its definition')
                    break

                #Create service object and auto verify everything else
                try:
                    service = Service(definition)
                except Exception as e:
                    print('[WARN] Service at ' + service_dir + ' failed to load:')
                    print(e)
                    break

                    services.append(service)
            else:
                print('[INFO] A file was found in the \'services\' directory. (Typically there should only be service folders)')

    @staticmethod
    def create_new_directory():

        if len(reusable_names) != 0:
            new_dir_number = reusable_names[0]
            reusable_names.remove(new_dir_number)
            new_dir = 'services/service' + str(new_dir_number)
            os.mkdir(new_dir)
            return new_dir


        for service in services:
            service_dir = service.directory

            dir_split = service.split('.', 1)

            if len(dir_split) != 2:
                print('[WARN] The service in directory ' + service_dir + ' does not follow III\'s folder method. It will be shutdown and removed from the service handler')
                service.stop_service()
                services.pop(service)

            try:
                if dir_split[1] != 'temp': #this shouldn't be neccessary, though idk if that will change in the future once an init method is added
                    top_number = int(dir_split[1])
            except:
                print('[WARN] The service in directory ' + service_dir + ' does not follow III\'s folder method. It will be shutdown and removed from the service handler')
                service.stop_service()
                services.pop(service)
        
        if len(services) == 0:
            new_dir_number = 1
        else:
            new_dir_number = top_number + 1
        

        new_dir = 'services/service' + str(new_dir_number)
        
        os.mkdir(new_dir)
        return new_dir
        
    @staticmethod
    def add_new_service(dir):
        #load service from definition

        definition = XMLService.load_definition(dir)

        if defnition == False:
            print('[WARN] The service located at ' + service_dir + ' failed to load its definition')
            return

        #Create service object and auto verify everything else
        try:
            service = Service(definition)
        except Exception as e:
            print('[WARN] Service at ' + service_dir + ' failed to load:')
            print(e)
            return

            services.append(service)

    @staticmethod
    def delete_service(dir, uaddress=None):
        
        for service in services:
            if dir == service.dir:
                service.stop_service()
                deletetree(dir)
                services.remove(service)
                return
            
            s_address = uaddress.split('.', 1)

            if s_address[0] == service.address and s_address[1] == service.name:
                service.stop_service()
                deletetree(dir)
                services.remove(service)
                return

        print('The service specified was not found')

    @staticmethod
    def copytree(src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    @staticmethod
    def deletetree(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    @staticmethod
    def list_services():
        service_list = ['Services installed:', '\n']

        for service in services:
            name = service.name
            uaddress = service.uaddress
            raw_status = service.process.poll()

            if (raw_status == None):
                status = "Alive"
            else:
                status = "Dead"

            item = '\nName: ' + name + ' uaddress: ' + uaddress + ' Status: ' + status
            service_list.append(item)

        return service_list


class Service:

   def __init__(self, data):
       #assumption data has been succesfully initilized and loaded from local definition first

       self.buffer = []
       self.status = False;
       self.display = False;

       #setup service data

       self.dir = data[0]
       self.version = data[1]
       self.counter = data[2]
       self.name = data[3]
       self.desc = data[4]
       self.address = data[5]
       self.dependencies = data[6]
       self.tags = data[7]
       delete = data[8]

       #parse tags
       for tag in tags:
           if tag[0] == 'application':
               self.type = tag[0]
               self.os_type = tag[1]
           elif tag[0] == 'resource':
               self.type = tag[0]

       #verify existence in peer node
       XMLService.verify_location(my_address, self.address, self.name)

       #check/verify against index 
       if XMLService.verify_definition(self.dir, self.version, self.counter, self.name, self.address) == False:
           raise Exception('[WARN] Sevrice does not match index definition (is there an update?)')

       #verify start files if required
       if self.type == 'application':
           iii_start_dir_windows = os.path.join(dir, 'iiistart.bat')
           iii_start_dir_posix = os.path.join(dir, 'iiistart.sh')

           if self.os_type == 'all':
               if not os.path.isfile(iii_start_dir_windows) and os.path.isfile(iii_start_dir_posix):
                   raise Exception('Missing start files for OS type all')
           elif self.os_type == 'nt':
               if not os.path.isfile(iii_start_dir_windows):
                   raise Exception('Missing start files for OS type Windows NT')
           elif self.os_type == 'linux':
               if not os.path.isfile(iii_start_dir_posix):
                   raise Exception('Missing start files for OS type Windows NT')

       #set start file based on current os
       if os_name == 'nt':
           self.start_file = os.path.abspath(self.iii_start_dir_windows)
       else:
           self.start_file = os.path.abspath(self.iii_start_dir_posix)   

   def start_service(self):
       self.process = subprocess.Popen([self.start_file], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       self.status = True;

       while(self.status):
           line = test_process.stdout.readline().decode('utf8')
           
           if self.display:
               print(line)
           else:
               self.buffer.append(line)

           if len(self.buffer) > 500:
               self.buffer.pop(0)

   def stop_service(self):
       self.status = False;
       self.process.kill()

   def restart_service(self): #Was this really neccesarry? Yes. Yes it was. Did I spell necessary incorrectly? Yes. Yes I did. Am I wasting time making useless comments? No! Of course not!
       self.stop_service()
       self.start_service()

