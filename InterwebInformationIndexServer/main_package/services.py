#Contains everything to load, run, handle services and etc.
import os
from os import name as os_name
import subprocess
from main_package.xml import XMLServiceDefinition
from main_package.cryptographer import Cryptographer
from lxml import etree as et
import time

class ServiceHandler:

    @staticmethod
    def main(address):

        #global handler_status
        #handler_status = True
        
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
                #attempt to load the service
                try:
                    rel_service_path = 'services/' + service_dir
                    service = Service(rel_service_path)

                    #verify that service is in peer node
                    service_pass = True

                    if XMLServiceDefinition.check_service(address, service.address, service.name) == False:
                        #raise Exception('Service is not in peer node')
                        print('[WARN] The service in the folder \"' + service.directory + '\" was not found in your peer node. III will not start it!')
                        service_pass = False

                    #verify service files match master node
                    if XMLServiceDefinition.verify_service(service.address, service.name, service.iii_dir) == False:
                        #raise Exception('Service files do not match master node')
                        print('[WARN] The service in the folder \"' + service.directory + '\" does not match with the master node. III will not start it!')
                        service_pass = False

                    if service_pass:
                        services.append(service)
                except:
                    print('[WARN] The service located in ' + service_dir + ' failed to load!')
            else:
                print('[INFO] A file was found in the \'services\' directory. (Typically there should only be service folders)')

    @staticmethod
    def create_new_directory():
        #DEBUG
        global reusable_names
        reusable_names = []


        if len(reusable_names) != 0:
            new_dir_number = reusable_names[0]
            reusable_names.pop(new_dir_number)
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
    def add_new_service(directory, address):
        #the address input is a debug

        try:
            service = Service(directory)

            #verify that service is in peer node
            service_pass = True

            if XMLServiceDefinition.check_service(address, service.address, service.name) == False:
                #raise Exception('Service is not in peer node')
                print('[WARN] The service in the folder \"' + service.directory + '\" was not found in your peer node. III will not start it!')
                service_pass = False

            #verify service files match master node
            if XMLServiceDefinition.verify_service(service.address, service.name, service.iii_dir) == False:
                #raise Exception('Service files do not match master node')
                print('[WARN] The service in the folder \"' + service.directory + '\" does not match with the master node. III will not start it!')
                service_pass = False

            if service_pass:
                services.append(service)
        except:
            print('[WARN] The service located in ' + directory + ' failed to load!')

    @staticmethod
    def delete_service(directory, name=None):
        
        for service in services:
            s_directory = service.directory
            s_name = service.name

            if directory != None:
                if s_directory == directory:
                    dir_split = s_directory.split('.', 1)
                    service_number = dir_split[1]

                    service.stop_service()
                    deletetree(directory)
                    services.pop(service)

                    reusable_names.append(service_number)
            elif name != None:
                if s_name == name:
                    dir_split = s_directory.split('.', 1)
                    service_number = dir_split[1]

                    service.stop_service()
                    deletetree(directory)
                    services.pop(service)
                    reusable_names.append(service_number)

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

   def __init__(self, directory, uaddress=None, new_service = False, name=None, desc=None):
       
       self.buffer = []
       self.status = False;
       self.display = False;

       self.directory = directory
       self.iii_dir = directory + '/.iii'
       self.iii_xml_dir = directory + '/.iii/iii.xml'
       self.iii_schema_dir = directory + '/.iii/iii.xsd'
       self.iii_uaddress_dir = directory + '/.iii/uaddress.txt'
       self.iii_start_dir_windows = directory + '/iiistart.bat'
       self.iii_start_dir_posix = directory + '/iiistart.sh'
           
       #check if required files and diretcories exist
       iii_exists = os.path.isdir(self.iii_dir)
       iii_xml_exists = os.path.isfile(self.iii_xml_dir)
       iii_schema_exists = os.path.isfile(self.iii_schema_dir)
       iii_uaddress_exists = os.path.isfile(self.iii_uaddress_dir)
       iii_start_windows_exists = os.path.isfile(self.iii_start_dir_windows)
       iii_start_posix_exists = os.path.isfile(self.iii_start_dir_posix)

       if (iii_exists and iii_xml_exists and iii_schema_exists):
           if (iii_start_windows_exists and iii_start_posix_exists):
               self.os_type = 'all'
           elif (iii_start_posix_exists or iii_start_windows_exists):
               if iii_start_posix_exists:

                   if os_name == 'nt':
                       print('[ERROR] No POSIX start file found (you are running on a GNU/Linux or Unix machine)')
                       raise Exception('No POSIX start file found')

                   self.os_type = 'posix'
               elif iii_start_windows_exists:

                   if os_name != 'nt':
                       print('[ERROR] No Windows start file found (you are running on a Windows machine)')
                       raise Exception('No Windows start file found')

                   self.os_type = 'nt'
           else:
               print('[ERROR] Service directory does not contain any start files!')
               raise Exception('Service directory does not contain any start files')
       else:
           print('[ERROR] Service directory does not contain proper defining files (check .iii folder)')
           raise Exception('Service directory does not conatin proper defining files')

       #check data if new service
       if new_service == True:
           self.new_service(directory, name, desc)
       else:
           try:
                temp_xml_data=XMLServiceDefinition.get_service_files(directory)
                self.service_version = Cryptographer.generate_hash(et.tostring(temp_xml_data).decode('utf8'))
           except:
                print('[WARN] The service III tried to initilize has errors!')
                raise Exception('Service files incorretcly configured')
 

       #parse iii.xml to ensure it passes schema and that all db files and directories defined exist
       with open(self.iii_xml_dir, 'r') as xml_file:
           xml_string = xml_file.read()

       self.variable_files = XMLServiceDefinition.parse_xml_string(xml_string, self.directory)

       if self.variable_files == False:
           print('[ERROR] Service definitions do not correlate to files (check iii.xml)')
           raise Exception('Service definitions do not correlate to files')

       #check if uaddress file needs to be created
       if iii_uaddress_exists:
           pass
       else:
           with open(self.iii_uaddress_dir, 'w') as uaddress_file:
               uaddress_file.write(uaddress)
               uaddress_file.close()

       #initialize address and name variables from uaddress
       with open(self.iii_uaddress_dir, 'r') as uaddress_file:
            uaddress_text = uaddress_file.read()
            uaddress_split = uaddress_text.split('.', 1)

            #add a thing to verify address follows correct format

            if len(uaddress_split) != 2:
                print('[ERROR] Service uaddress file is malformed!')
                raise Exception('Uaddress file is malformed')
            else:
                self.address = uaddress_split[0]
                self.name = uaddress_split[1]
                self.uaddress = uaddress_text

       #set start file based on current os
       if os_name == 'nt':
           self.iii_service_start_path = os.path.abspath(self.iii_start_dir_windows)
       else:
            self.iii_service_start_path = os.path.abspath(self.iii_start_dir_posix)
   
   def new_service(self, directory, name, desc):

       try:
           xml_data_object=XMLServiceDefinition.get_service_files(directory)
       except:
           print('[WARN] The service you tried to initilize has errors (check iii.xml)!')
           raise Exception('New service files incorretcly configured')

       self.service_version = Cryptographer.generate_hash(et.tostring(xml_data_object).decode('utf8'))
       self.service_xml_object = XMLServiceDefinition.create_new_service(xml_data_object, name, desc)

   def start_service(self):
       self.process = subprocess.Popen([self.iii_service_start_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

class Service2:

   def __init__(self, data):
       
       self.buffer = []
       self.status = False;
       self.display = False;

       #setup service data

       self.dir = data[0]
       self.version = data[1]
       self.counter = data[2]
       self.name = data[3]
       self.desc = data[4]
       self.dependencies = data[5]
       self.tags = data[6]
       delete = data[7]

       #parse tags
       for tag in tags:
           if tag[0] == 'application':
               self.type = tag[0]
               self.os_type = tag[1]
           elif tag[0] == 'resource':
               self.type = tag[0]

       #check/verify against index 

       #verify start files if required

       #check data if new service
       if new_service == True:
           self.new_service(directory, name, desc)
       else:
           try:
                temp_xml_data=XMLServiceDefinition.get_service_files(directory)
                self.service_version = Cryptographer.generate_hash(et.tostring(temp_xml_data).decode('utf8'))
           except:
                print('[WARN] The service III tried to initilize has errors!')
                raise Exception('Service files incorretcly configured')
 

       #parse iii.xml to ensure it passes schema and that all db files and directories defined exist
       with open(self.iii_xml_dir, 'r') as xml_file:
           xml_string = xml_file.read()

       self.variable_files = XMLServiceDefinition.parse_xml_string(xml_string, self.directory)

       if self.variable_files == False:
           print('[ERROR] Service definitions do not correlate to files (check iii.xml)')
           raise Exception('Service definitions do not correlate to files')

       #check if uaddress file needs to be created
       if iii_uaddress_exists:
           pass
       else:
           with open(self.iii_uaddress_dir, 'w') as uaddress_file:
               uaddress_file.write(uaddress)
               uaddress_file.close()

       #initialize address and name variables from uaddress
       with open(self.iii_uaddress_dir, 'r') as uaddress_file:
            uaddress_text = uaddress_file.read()
            uaddress_split = uaddress_text.split('.', 1)

            #add a thing to verify address follows correct format

            if len(uaddress_split) != 2:
                print('[ERROR] Service uaddress file is malformed!')
                raise Exception('Uaddress file is malformed')
            else:
                self.address = uaddress_split[0]
                self.name = uaddress_split[1]
                self.uaddress = uaddress_text

       #set start file based on current os
       if os_name == 'nt':
           self.iii_service_start_path = os.path.abspath(self.iii_start_dir_windows)
       else:
            self.iii_service_start_path = os.path.abspath(self.iii_start_dir_posix)
   
   def new_service(self, directory, name, desc):

       try:
           xml_data_object=XMLServiceDefinition.get_service_files(directory)
       except:
           print('[WARN] The service you tried to initilize has errors (check iii.xml)!')
           raise Exception('New service files incorretcly configured')

       self.service_version = Cryptographer.generate_hash(et.tostring(xml_data_object).decode('utf8'))
       self.service_xml_object = XMLServiceDefinition.create_new_service(xml_data_object, name, desc)

   def start_service(self):
       self.process = subprocess.Popen([self.iii_service_start_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

