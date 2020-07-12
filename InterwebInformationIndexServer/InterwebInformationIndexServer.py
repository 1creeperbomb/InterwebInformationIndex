#oh yeahhhhhh

from main_package.cryptographer import Cryptographer
from main_package.xml import XMLIndex
from main_package.network import SocketServer

import multiprocessing
import time

from os import system, name 
import os.path
from getpass import getpass

processes = []
crypto_main = None

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

    crypto_main = Cryptographer(private_key, False)
    password = None
    private_key = None
    
    print('-----------------------------------------------------')

    print('Attempting to start the network service!')
    network_process = multiprocessing.Process(target=SocketServer.main)

    network_process.start()
    processes.append(network_process)
    time.sleep(5)

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

        pass
    elif type == 'string':
        pass
    elif type == 'int':
        pass
    elif type == 'menu':

        if input in ['0','1','2','3','4','5','6','0?','1?','2?','3?','4?','5?','6?']:
            return input
        else:
            return False;

def clear():

    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear') 

def print_menu():
    print('Select an option. To see what each option does, type the option number followed by a \"?\" (ex: 3?): ')
    print('[1] Create a master node')
    print('[2] Create a peer node') 
    print('[3] Create a service to host')
    print('[4] Select a service to help host')
    print('[5] Start/Restart the network process')
    print('[6] Stop the network process')
    print('[0] Exit III')

def browse_menu():
    print_menu()
    selection = input('Select: ')

    while(filter_input(selection, 'menu') == False):
        clear()
        print_menu()
        print('Please enter a valid option!')
        selection = input('Select: ')
        filter_input(selection, 'menu')

    #so like, does python have a switch case? Or should I just spam elif lmao?
    
    if selection == '0':
        #shutdown
        shutdown(processes)
    elif selection == '1':

        address = crypto_main.public_key





        pass
    elif selection == '2':
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
        print('[1] This will allow you to publish services that other peers can then help host (use option 3 after setting this up)')
        pause_key()
    elif selection == '2?':
        clear()
        print('[2] This will allow you to help host services from a master node (use option 4 after setting this up) (NOTE: You also need to create a peer node if you have a master node so that other peers can copy the required files)')
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
    clear()
    browse_menu()

def pause_key():
    input("Press Enter to continue...")

def first_time_setup():
    password = getpass('Please enter a strong password to encrypt your private key: ')

    password_check = getpass('Please eneter the password again to verify: ')

    while password != password_check:
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


