#Menu and CLI classes
from os import system, name as os_name
import argparse

menu_open = False;

class Menu:

    @staticmethod
    def filter_input(input, type):
        if type == 'y/n':
            
            if input == 'y' or input == 'n' or input == 'Y' or input == 'N':
                input = input.lower()
                return input
            else:
                return False;

        elif type == 'menu':

            if input in ['0','1','2','3','4','5','6','7','0?','1?','2?','3?','4?','5?','6?','7?']:
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
            if len(input) <= 1000 and len(input) > 0:
                return input
            else:
                return False
        elif type == 'node_type':

            if input in ['master', 'peer']:
                return input
            else:
                return False
    
    @staticmethod
    def print_menu(menu_type):
    
        if menu_type == 'main':
            print('Select an option. To see what each option does, type the option number followed by a \"?\" (ex: 3?): ')
            print('[1] Create a master or peer node')
            print('[2] Modify a master or peer node') 
            print('[3] Delete a master or peer node')
            print('[4] Start/Restart/Stop an III service')
            print('[5] Connect to an III service')
            print('[6] Start/Restart/Stop an III process (ADVANCED)')
            print('[7] Exit III')
            print('[0] Exit Menu')
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

    @staticmethod
    def pause_key():
        #Pause for menu
        input("Press Enter to continue...")

    @staticmethod
    def clear():

        if os_name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear') 

class CLI:

    buffer = []

    def main():
        parser = argparse.ArgumentParser()
        parser.parse_args()


