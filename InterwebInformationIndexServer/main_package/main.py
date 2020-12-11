#handles multiprocessing and takes input from CLI and Menu
from main_package.cryptographer import Cryptographer
#from main_package.network import SocketServer
#from main_package.network import ConnectionHandler
from main_package.services import Service
from main_package.ftp import FTP
from main_package.menu import Menu, CLI
from main_package.xml import XMLIndex
from main_package.processes import ProcessHandler

import multiprocessing
import time
import shutil
import os.path
from os import system, name as os_name
from getpass import getpass

class Main:

    @staticmethod
    def start():
        
        global process_handler
        process_handler =  multiprocessing.Process(target=ProcessHandler.main)

        global processes
        processes = []

        print('Starting the Interweb Information Index Server (III)!')
        print('-----------------------------------------------------')
        print('Created by Ismaeel Mian (1creeperbomb)')
        print('-----------------------------------------------------')
        print('Check out/contribute the the project on github at https://github.com/1creeperbomb/InterwebInformationIndex')
        print('----------------------------------------------------------------------------------------------------------')

        #check if private key file exists
        if os.path.isfile('keystore/private.key'):
            print('Private key found! Starting normal operation!')
        else:
            print('No private key files was found. If you are importing a key, make sure the file is named \"private.key\" and is located directly in the \"keystore\" folder')
            start_setup = filter_input(input('Would you like to setup a new keypair? (Y/N): '), 'y/n')

            while filter_input(start_setup, 'y/n') == False:
                print('Please enter a valid choice')
                start_setup == input('Would you like to setup a new keypair? (Y/N): ')

            if start_setup == 'y':
                first_time_setup()
            elif start_setup == 'n':
                print('You chose no')
                shutdown(None)

        password = getpass('Please enter your password to start: ')

        try:
            print('Attempting to decrypt...')
            private_key = Cryptographer.read_key(password)
            print('Succesfully decrypted!')
        except:
            print('Failed to decrypt!')
            shutdown(None)

        global crypto_main
        crypto_main = Cryptographer(private_key, False)
        password = None
        private_key = None
    
        print('-----------------------------------------------------')

        #start services

        print('[INFO] Attempting to start iii sub processes...')
        process_handler.start()
        #processes.append(process_handler)
        time.sleep(4)

        #print('Attempting to start the network service!')
        #network_process = multiprocessing.Process(target=SocketServer.main)

        #network_process.start()
        #processes.append(network_process)
        #time.sleep(4)
        #print(network_process.is_alive())

        #print('Attempting to start the service handler!')
        #service_handler = multiprocessing.Process(target=ServiceHandler.main("test"))
        #processes.append(service_handler)
        #time.sleep(4)

        #debug starts
        #ConnectionHandler.main()

        Menu.clear()

        Main.browse_menu()

    @staticmethod
    def load_screen(type):

        if type == 'Menu':
            Menu.clear()
            Menu.browse_menu()
        elif type == 'CLI':
            pass
        else:
            #parse as name or uaddress

            if len(type) > 44:
                #parse uaddress
                for service in ServiceHandler.services:
                    service_uaddress = service.uaddress

                    if type == uaddress:
                        Menu.clear()
                        for line in service.buffer:
                            print(line)

                        service.display = True
                        Main.forwrad_input(service)
                    else:
                        print('The service you entered was not found!')
                        
            else:
                for service in ServiceHandler.services:
                    name = service.name
                    found = []

                    if type == name:
                        found.append(service)

                    if len(found) == 0:
                        print('The service you entered was not found!')
                    elif len(found) == 1:
                        Menu.clear()
                        for line in service.buffer:
                            print(line)

                        service.display = True
                        Main.forwrad_input(service)
                    elif len(found) > 1:
                        print('Multiple services with that name were found:')
                        for service in found:
                            name = service.name
                            uaddress = service.uaddress
                            item = '\nName: ' + name + ' uaddress: ' + uaddress
                            print(item)

    @staticmethod
    def browse_menu():
        Menu.print_menu('main')
        selection = input('Select: ')

        while(Menu.filter_input(selection, 'menu') == False):
            Menu.clear()
            print_menu('main')
            print('Please enter a valid option!')
            selection = input('Select: ')
            Menu.filter_input(selection, 'menu')

        #so like, does python have a switch case? Or should I just spam elif lmao?
    
        if selection == '0':
            #exit menu
            pass
        elif selection == '1':

            address = crypto_main.get_public_key()

            node_type = Menu.filter_input(input('Please enter the type of node you want to create (master or peer): '), 'node_type')

            while node_type == False:
                print('Please enter a proper node type!')
                node_type = Menu.filter_input(input('Please enter the type of node you want to create (master or peer): '), 'node_type')

            name = Menu.filter_input(input('Enter a name for your node (40 characters max): '), 'name')

            while name == False:
                print('Please enter a proper name!')
                name = Menu.filter_input(input('Enter a name for your node (40 characters max): '), 'name')

            desc = Menu.filter_input(input('Enter a description for your node (1000 characters max): '), 'desc')

            while desc == False:
                print('Please enter a proper description!')
                desc = Menu.filter_input(input('Enter a description for your node (1000 characters max): '), 'desc')

            xml_data = XMLIndex.create_node(node_type, crypto_main, name, desc)

            ConnectionHandler.send_data(xml_data)

            pass
        elif selection == '2':

            node_type = Menu.filter_input(input('Please enter the type of node you want to modify (master or peer): '), 'node_type')

            while node_type == False:
                print('Please enter a proper node type!')
                node_type = Menu.filter_input(input('Please enter the type of node you want to modify (master or peer): '), 'node_type')

            #check if node exists
            address = crypto_main.get_public_key()
            node_check = XMLIndex.get_data(node_type, address)

            if node_check == None:
                print('You do not have a ' + node_type + ' node published!')
                time.sleep(3)
                Menu.clear()
                browse_menu()

            #browse node menu
            Menu.clear()
            Main.browse_node_edit_menu(node_type)

        elif selection == '3':
            pass
        elif selection == '4':
            

            service_id = input('Enter a service name or uaddress from the list: ')

        elif selection == '5':
            #print(ServiceHandler.list_services())
            pass
        elif selection == '7':
            Main.shutdown(processes)
            pass
        elif selection == '0?':
            Menu.clear()
            print('[0] This will exit the menu and return you to the CLI')
        elif selection == '1?':
            Menu.clear()
            print('[1] Creating a master node will allow you to publish services that other peers can then help host (use option 3 after setting this up)')
            print('Creating a peer node will allow you to help host services from a master node (use option 4 after setting this up)')
            print('(NOTE: You also need to create a peer node if you have a master node so that other peers can copy the required files)')
        elif selection == '2?':
            Menu.clear()
            print('[2] Modifying a master node will allow you to add/define services that other peers can then help host')
            print('Modifying a peer node will allow you to select services to help host from another master node')
            print('Modifying a node will also alow you to change the name and description')
        elif selection == '3?':
            Menu.clear()
            print('[3] This will create a service based off a directory and iii.xml file that will then be added to your master node')
        elif selection == '4?':
            Menu.clear()
            print('[4] This will allows you to start, restart, or stop a specefic III service you are helping to host')
        elif selection == '5?':
            Menu.clear()
            print('[5] This will connect you to a specefic III service so you can directly interact with it through the console (useful for setup, configuration, or sending commands)')
        elif selection == '6?':
            Menu.clear()
            print('[6] This will allows you to start, restart, or stop an III process such as the Netowrk Process, Service Handler, or Connection Handler.')
            print('Note that this is mostly useful for debugging or to restart a certain process without the need to completly restart III')
            print('Use with caution as stopping certain services will prevent certain functions in the menu from working!')
        elif selection == '7?':
            Menu.clear()
            print('[7] This will shutdown the III program as well as its sub processes and services')


        #after completing, menu appears again

        Menu.pause_key()

        Menu.clear()
        Main.browse_menu()

    @staticmethod
    def browse_node_edit_menu(node_type):

        if node_type == 'master':
                node_menu_type = 'node_edit_master'
        elif node_type == 'peer':
                node_menu_type = 'node_edit_peer'

        Menu.print_menu(node_menu_type)

        selection = input('Select: ')

        while(Menu.filter_input(selection, node_menu_type) == False):
            Menu.clear()
            Menu.print_menu(node_menu_type)
            print('Please enter a valid option!')
            selection = input('Select: ')
            Menu.filter_input(selection, 'menu')

        if selection == '0':
            return
        elif selection == '1':
        
            name = Menu.filter_input(input('Enter a new name for your node (40 characters max): '), 'name')

            while name == False:
                print('Please enter a proper name!')
                name = Menu.filter_input(input('Enter a new name for your node (40 characters max): '), 'name')

            address = crypto_main.get_public_key()

            new_node = XMLIndex.modify_node(node_type, crypto_main, address, name = name)

            ConnectionHandler.send_data(new_node)

        elif selection == '2':

            desc = Menu.filter_input(input('Enter a new description for your node (500 characters max): '), 'desc')

            while desc == False:
                print('Please enter a proper description!')
                desc = Menu.filter_input(input('Enter a new description for your node (500 characters max): '), 'desc')

            address = crypto_main.get_public_key()

            new_node = XMLIndex.modify_node(node_type, crypto_main, address, description_text = desc)

            ConnectionHandler.send_data(new_node)

        elif selection == '3':

            if node_type == 'master':

                name = Menu.filter_input(input('Enter a name for your service (40 characters max): '), 'name')

                while name == False:
                    print('Please enter a proper name!')
                    name = Menu.filter_input(input('Enter a name for your service (40 characters max): '), 'name')

                desc = Menu.filter_input(input('Enter a description for your service (1000 characters max): '), 'desc')

                while desc == False:
                    print('Please enter a proper description!')
                    desc = Menu.filter_input(input('Enter a description for your service (1000 characters max): '), 'desc')

                new_service_directory = input('Enter the root directory of your service files: ')

                if os.path.exists(new_service_directory) and os.path.isdir(new_service_directory): #redundant?
                    #uaddress
                    address = crypto_main.get_public_key()
                    uaddress = address + '.' + name

                    try:

                        #copy to service.temp to verify .iii stuff 
                        new_service_directory = os.path.realpath(new_service_directory)
                        temp_service = os.path.realpath('services/service.temp') 

                        try:
                            Main.deletetree(temp_service)
                            Main.copytree(new_service_directory, temp_service) 
                            #shutil.copytree(new_service_directory, temp_service) Will fail if dest diretcory already exists
                        except:
                            print('[ERROR] III was unable to copy the service files to it own directory (check folder permissions)')
                            input('Press Enter to return to the menu...')
                            return

                        new_service = Service('services/service.temp', uaddress, True, name, desc)
                    
                        #modify master node to add service data
                        service_xml_data = [new_service.service_xml_object]

                        new_node = XMLIndex.modify_node('master', crypto_main, address, name=None, description_text=None, services_n = service_xml_data)

                        #create new diretcory and copy files over
                        service_directory = ServiceHandler.create_new_directory()
                        Main.copytree(temp_service, os.path.realpath(service_directory))
                        Main.deletetree(temp_service)

                        del new_service #gets rid of temp service
                        #ServiceHandler.add_new_service(service_directory, address)
                        ConnectionHandler.send_data(new_node)

                    except:
                        print('[WARN] The service you tried to define does not conform to III standards (see warning above)')
                        input('Press Enter to return to the menu...')

                else:
                    print('[WARN] The directory you entered was not valid!')
                    input('Press Enter to return to the menu...')

            elif node_type == 'peer':

                uaddress = input('Please enter the uaddress of the service you would like to help host (format is \"address.service-name\"): ')
                peer_service_data = XMLIndex.get_from_uaddress(uaddress)

                #ensure service exists
                while peer_service_data == False:
                    print('Service does not exist! Please enter a valid uaddress or enter 0 to exit')
                    uaddress = input('Please enter the uaddress of the service you would like to help host (format is \"address.service-name\"): ')

                    if uaddress == '0':
                        return

                peer_service_data = XMLIndex.get_from_uaddress(uaddress)
                services = []
                services.append(peer_service_data)

                address = crypto_main.get_public_key()
                new_node = XMLIndex.modify_node(node_type, crypto_main, address, services_n=services)

                ConnectionHandler.send_data(new_node)
            
        elif selection == '4':
            pass
        elif selection == '0?':
            Menu.clear()
            print('This returns to the previous menu (duh?)')
            Menu.pause_key()
        elif selection == '1?':
            Menu.clear()
            print('This changes the node name (doyee?)')
            Menu.pause_key()
        elif selection == '2?':
            Menu.clear()
            print('This changes the node description (again, duh?)')
            Menu.pause_key()
        elif selection == '3?':
            Menu.clear()
            if node_type == 'master':
                print('This will allow you to define a service for your master node')
            elif node_type == 'peer':
                print('This will allow you to select a service for your peer node to help host')
            Menu.pause_key()
        elif selection == '4?':
            Menu.clear()
            print('This will allow you to edit/redefine/delete a service from your master node')
            Menu.pause_key()

        input('PAUSE')
        Menu.clear()
        Main.browse_node_edit_menu(node_type)
    
    @staticmethod
    def forwrad_input(service):
        escape = False;

        while escape == False:
            input = input()

            if input == '//disconnect':
                escape = True
            else:
                service.process.stdin.write(input.encode('utf8'))
        
        Main.load_screen(Menu)

    @staticmethod
    def shutdown(processes):

        if processes == None:
            pass
        else:
            for process in processes:
                process.terminate()
                process.join()

        print('Shutting down...')
        print('Goodbye!')
        exit()

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