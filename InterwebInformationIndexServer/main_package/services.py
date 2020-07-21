#Contains everything to load, run, handle services and etc.
import os
from os import name as os_name
import subprocess
from main_package.xml import XMLServiceDefinition
from main_package.cryptographer import Cryptographer

class ServiceHandler:

    services = []

    def main(address):
        #initilize services from service folder

        services_dir = os.listdir('services')

        for service_dir in services_dir:
            if os.path.isdir(service_dir):
                #attempt to load the service
                try:
                    service = Service(services_dir)

                    #verify that service is in peer node
                    service_pass= True

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
                print('[INFO] A file was found in the \'services\' diretcory. (Typically there should only be service folders)')
        

class Service:

   def __init__(self, directory, uaddress=None, new_service = None):
       
       self.directory = directory
       self.iii_dir = directory + '/.iii'
       self.iii_xml_dir = directory + '/.iii/iii.xml'
       self.iii_schema_dir = directory + '/.iii/iii.xsd'
       self.iii_uaddress_dir = directory + '/.iii/uadress.txt'
       self.iii_start_dir_windows = directory + '/iiistart.bat'
       self.iii_start_dir_posix = directory + '/iiistart.sh'
           
       #check if required files and diretcories exist
       iii_exists = os.path.isdir(iii_dir)
       iii_xml_exists = os.path.isfile(iii_xml_dir)
       iii_schema_exists = os.path.isfile(iii_schema_dir)
       iii_uaddress_exists = os.path.isfile(iii_uaddress_dir)
       iii_start_windows_exists = os.path.isfile(iii_start_dir_windows)
       iii_start_posix_exists = os.path.isfile(iii_start_dir_posix)

       if (iii_exists and iii_xml_existts and iii_schema_exists and iii_uaddress_exists):
           if (iii_start_windows_exists and iii_start_posix_exists):
               self.os_type = 'all'
           elif (iii_start_posix_exists or iii_start_windows_exists):
               if iii_start_posix_exist:

                   if os_name == 'nt':
                       raise Exception('No POSIX start file found')

                   self.os_type = 'posix'
               elif iii_start_windows_exists:

                   if os_name != 'nt':
                       raise Exception('No Windows start file found')

                   self.os_type = 'nt'
           else:
               raise Exception('Service diretcory does not conatin proper defining files')
       else:
           raise Exception('Service diretcory does not conatin proper defining files')

       #check data if new service
       if new_service == True:
           new_service(directory)

       #parse iii.xml to ensure it passes schema and that all db files and directories defined exist
       with open(self.iii_xml_dir, 'r') as xml_file:
           xml_string = xml_file.read()

       self.variable_files = XMLServiceDefinition.parse_xml_string(xml_string, self.directory)

       if variable_files == False:
           raise Exception('Service defnitions do not correlate to files')

       #check if uaddress file needs to be created
       if iii_uaddress_exists:
           pass
       else:
           with open(iii_uaddress_dir, 'w') as uaddress_file:
               uaddress_file.write(uaddress)
               uaddress_file.close()

       #initialize address and name variables from uaddress
       with open(iii_uaddress_dir, 'r') as uaddress_file:
            uaddress_text = uaddress_file.read()
            uaddress_split = uaddress_text.split('.', 1)

            if len(uaddress_split != 2):
                raise Exception('Uaddress file is malformed')
            else:
                self.address = uaddress_split[0]
                self.name = uaddress_split[1]

       #set start file based on current os
       if os_name == 'nt':
           self.iii_service_start_path = os.path.abspath(self.iii_start_dir_windows)
       else:
            self.iii_service_start_path = os.path.abspath(self.iii_start_dir_posix)
   
   def new_service(self, directory):

       try:
           self.xml_data=XMLServiceDefinition.get_service_files(directory)
       except:
           print('[WARN] The service you tried to initilize has errors!')

       self.service_version = Cryptographer.generate_hash(self.xml_data)



   def start_service(self):
       self.process = subprocess.Popen([self.iii_service_start_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

   def stop_service(self):
       self.process.kill()

   def restart_service():
       self.stop_service()
       self.start_service()

