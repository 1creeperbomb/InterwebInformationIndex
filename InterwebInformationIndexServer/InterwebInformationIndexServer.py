#oh yeahhhhhh

from main_package.cryptographer import Cryptographer
from main_package.xml import XMLIndex
from main_package.network import SocketServer
from main_package.network import ConnectionHandler

import multiprocessing
import time

from os import system, name 
import os.path
from getpass import getpass

processes = []

def main(): #this must be the main method in the main class so that it can handle the processes in a list
    

    #Fun fact: I was listening to Zame's DPP remastered music while coding this lol

    print('Starting the Interweb Information Index Server (III)!')
    print('-----------------------------------------------------')
    print('Created by Ismaeel Mian (1creeperbomb)')
    print('-----------------------------------------------------')
    print('Check out/contribute the the project on github at https://github.com/1creeperbomb/InterwebInformationIndex')
    print('-----------------------------------------------------')

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

    print('Attempting to start the network service!')
    network_process = multiprocessing.Process(target=SocketServer.main)

    network_process.start()
    processes.append(network_process)
    time.sleep(4)

    #debug starts
    ConnectionHandler.main()

    clear()

    browse_menu()



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
    

def filter_input(input, type):
    if type == 'y/n':
            
        if input == 'y' or input == 'n' or input == 'Y' or input == 'N':
            input = input.lower()
            return input
        else:
            return False;

    elif type == 'menu':

        if input in ['0','1','2','3','4','5','6','0?','1?','2?','3?','4?','5?','6?']:
            return input
        else:
            return False;
    elif type == 'node_edit_master':

        if input in ['0','1','2','3','4','0?','1?','2?','3?','4?']:
            return input
        else:
            return False;
    elif type == 'node_edit_peer':

        if input in ['0','1','2','3','0?','1?','2?','3?']:
            return input
        else:
            return False;
    elif type == 'name':

        if len(input) <= 40 and len(input) > 0:
            return input
        else:
            return False

    elif type == 'desc':
        if len(input) <= 500 and len(input) > 0:
            return input
        else:
            return False
    elif type == 'node_type':

        if input in ['master', 'peer']:
            return input
        else:
            return False

def clear():

    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear') 

def print_menu(menu_type):
    
    if menu_type == 'main':
        print('Select an option. To see what each option does, type the option number followed by a \"?\" (ex: 3?): ')
        print('[1] Create a master or peer node')
        print('[2] Modify a master or peer node') 
        print('[3] Delete a master or peer node')
        print('[4] empty')
        print('[5] Start/Restart the network process')
        print('[6] Stop the network process')
        print('[0] Exit III')
    elif menu_type == 'node_edit_master':
        print('Select an option. To see what each option does, type the option number followed by a \"?\" (ex: 3?): ')
        print('[1] Change node name')
        print('[2] Change node description')
        print('[3] Define a service to publish on the index')
        print('[4] Edit the details of a service')
        print('[0] Back')
    elif menu_type == 'node_edit_peer':
        print('Select an option. To see what each option does, type the option number followed by a \"?\" (ex: 3?): ')
        print('[1] Change node name')
        print('[2] Change node description')
        print('[3] Choose a service to help host')
        print('[0] Back')

def browse_menu():
    print_menu('main')
    selection = input('Select: ')

    while(filter_input(selection, 'menu') == False):
        clear()
        print_menu('main')
        print('Please enter a valid option!')
        selection = input('Select: ')
        filter_input(selection, 'menu')

    #so like, does python have a switch case? Or should I just spam elif lmao?
    
    if selection == '0':
        #shutdown
        shutdown(processes)
    elif selection == '1':

        address = crypto_main.get_public_key()

        node_type = filter_input(input('Please enter the type of node you want to create (master or peer): '), 'node_type')

        while node_type == False:
            print('Please enter a proper node type!')
            node_type = filter_input(input('Please enter the type of node you want to create (master or peer): '), 'node_type')

        name = filter_input(input('Enter a name for your node (40 characters max): '), 'name')

        while name == False:
            print('Please enter a proper name!')
            name = filter_input(input('Enter a name for your node (40 characters max): '), 'name')

        desc = filter_input(input('Enter a description for your node (500 characters max): '), 'desc')

        while desc == False:
            print('Please enter a proper description!')
            desc = filter_input(input('Enter a description for your node (500 characters max): '), 'desc')

        xml_data = XMLIndex.create_node('master', crypto_main, name, desc)

        ConnectionHandler.send_data(xml_data)

        pass
    elif selection == '2':

        node_type = filter_input(input('Please enter the type of node you want to modify (master or peer): '), 'node_type')

        while node_type == False:
            print('Please enter a proper node type!')
            node_type = filter_input(input('Please enter the type of node you want to modify (master or peer): '), 'node_type')

        #browse node menu
        clear()
        browse_node_edit_menu(node_type)


        pass
    elif selection == '3':
        pass
    elif selection == '4':
        pass
    elif selection == '0?':
        clear()
        print('[0] This will shutdown the III program as well as its sub processes and services')
        pause_key()
    elif selection == '1?':
        clear()
        print('[1] Creating a master node will allow you to publish services that other peers can then help host (use option 3 after setting this up)')
        print('Creating a peer node will allow you to help host services from a master node (use option 4 after setting this up)')
        print('(NOTE: You also need to create a peer node if you have a master node so that other peers can copy the required files)')
        pause_key()
    elif selection == '2?':
        clear()
        print('[2] Modifying a master node will allow you to add/define services that other peers can then help host')
        print('Modifying a peer node will allow you to select services to help host from another master node')
        print('Modifying a node will also alow you to change the name and description')
        pause_key()
    elif selection == '3?':
        clear()
        print('[3] This will create a service based off a directory and iii.xml file that will then be added to your master node')
        pause_key()
    elif selection == '4?':
        clear()
        print('[4] This will sync the required files of the service you would like to help host')
        pause_key()
    elif selection == '5?':
        clear()
        print('[5] This will attempt to start the network process. If the process is already running, it will attempt to restart')
        pause_key()
    elif selection == '6?':
        clear()
        print('[6] This will stop the network process')
        pause_key()

    #after completing, menu appears again

    input('Paused...')

    clear()
    browse_menu()


def browse_node_edit_menu(node_type):

    if node_type == 'master':
            node_menu_type = 'node_edit_master'
    elif node_type == 'peer':
            node_menu_type = 'node_edit_peer'

    print_menu(node_menu_type)

    selection = input('Select: ')

    while(filter_input(selection, node_menu_type) == False):
        clear()
        print_menu(node_menu_type)
        print('Please enter a valid option!')
        selection = input('Select: ')
        filter_input(selection, 'menu')

    if selection == '0':
        return
    elif selection == '1':
        print('Heyyyyyyyooooooooooo')
        time.sleep(5)
        pass
    elif selection == '2':
        pass
    elif selection == '3':
        pass
    elif selection == '4':
        pass

    clear()
    browse_node_edit_menu(node_type)




def pause_key():
    input("Press Enter to continue...")

def first_time_setup():
    password = getpass('Please enter a strong password to encrypt your private key: ')

    password_check = getpass('Please eneter the password again to verify: ')

    while password != password_check or len(password) == 0:
        password = getpass('Passwords did not match, try again! Please enter a strong password to encrypt your private key: ')

        password_check = getpass('Please eneter the password again to verify: ')

    try:
        Cryptographer.generate_keypair(password)
        print('Key scuccessfully generated and encrypted in private.key. Remember your password or make sure you have saved it to a good password manager!')
    except:
        print('Failed to generate and encrypt a new private key! Does the keystore folder have proper permissions setup?')

    password = None #I have no idea if this is really necessary because Python does garbge collection anyway lol
    password_check = None

if __name__ == '__main__':
    main()


