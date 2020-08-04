import base64
import random
import string
import os
import glob
from lxml import etree as et
from io import StringIO, BytesIO
from main_package.cryptographer import Cryptographer

class XMLIndex:
    #methods

    @staticmethod
    def get_xml_type(xml_data_raw):
        try:
            root = et.fromstring(xml_data_raw)
            return root.tag
        except:
            print('XML is malformed!')
            return None

    @staticmethod
    def parse_xml_string(xml_data_raw):
        #all elements must have xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance in the root for the signature verification to work

        #read the xml schema and create a schema object
        with open('index-schema.xsd', 'r') as schema_file:
            schema_raw = et.XML(schema_file.read())
            schema = et.XMLSchema(schema_raw)

        #add data to a root element
        root = et.Element("root")
        root.append(et.XML(xml_data_raw))
        xml_data = et.tostring(root)

        parser = et.XMLParser(schema = schema)

        try:
            root = et.fromstring(xml_data, parser)
        except:
            print('Schema validation failed!')
            return False

        #verify address
        root = et.fromstring(xml_data_raw)

        #check iii data version
        if root.attrib['iiiVersion'] != '1':
            print('Node is not from this version and not supported')
            return False;

        node_type = root.tag
        services =[]

        for child in root:
            if child.tag == 'address':
                address = child.text
            elif child.tag == 'sign':
                signature = child.text
                salt = child.attrib['salt']
            elif child.tag == 'services':
                data = et.tostring(child).decode('utf8')

                for service in child:
                    services.append(service)

        try:
            crypto = Cryptographer(address, True)
            if crypto.verify_data(data, signature, salt):
                print('Signature verified successfully!')
            else:
                print('Signature failed to verify')
                return False
        except:
            print('Invalid key / key is corrupt')
            return False

        services_copy = services.copy()

        #verify counter is latest
        check = XMLIndex.get_data(node_type, address)[0]
        if check != None:
            for child in check:
                if child.tag == 'services':

                    for check_service in child:
                        check_version = check_service.attrib['version']
                        check_counter = int(check_service.attrib['counter'])

                        for service in services_copy:
                            version = check_service.attrib['version']
                            counter = int(service.attrib['counter'])

                            if check_version == version:
                                if counter > check_counter:
                                    services_copy.remove(service)

        if len(services_copy) != 0:
            print('Service counters do not match!')
            return False

        #parse any special tags
        for service in services:
            for child in service:
                if child.tag == 'tags':
                    for tag in child:
                        
                        if tag.tag == 'DELETE':

                            service.getparent().remove(service)

        #send data to write method and socket sever
        XMLIndex.__write_xml(et.tostring(root).decode('utf8'), address, node_type)

        return True

    @staticmethod
    def get_data(xpath, address=None, tree=None):
        #tree must be passed through so .remove() will work since it bases it on direct memeory location

        if tree == None:
            parser = et.XMLParser(remove_blank_text=True)
            tree = et.parse('index.xml', parser)

        #relative path format example: master/services/desc
        #first get full xpath
        if address != None:
            xpath = XMLIndex.__get_xpath(address, xpath)

        #retrieve the data and return
        #ns = {'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance"}
        #namespaces=ns
        try:
            data = tree.xpath(xpath)
        except:
            return None

        #this will return either the data as a string or the associated data element or None if the data could not be found'

        try:
            data[0]
        except:
            return None

        return data

    @staticmethod
    def create_node(type, crypto, name, description_text):
        if type == 'master':
            root = et.Element('master')
        elif type == 'peer':
            root = et.Element('peer')

        address_text = crypto.get_public_key()

        address_element = et.SubElement(root, 'address')
        address_element.text = address_text

        salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))

        signature = et.SubElement(root, 'sign')
        signature.set('salt', salt)

        description = et.SubElement(root, 'desc')
        description.set('name', name)
        description.text = description_text

        services = et.SubElement(root, 'services')

        #add default services if applicable

        #add default tags if applicaple 

        #sign services data
        raw_data = et.tostring(services).decode('utf8')

        signed_data = crypto.sign_data(raw_data, salt)

        signature.text = signed_data

        string_xml = et.tostring(root).decode('utf8')

        return string_xml

    @staticmethod
    def modify_node(type, crypto, address, name=None, description_text=None, services_n=None):
        node = XMLIndex.get_data(type, address)[0]
        XMLIndex.get_data('master', address)

        print(node)

        for child in node:
            if child.tag == 'desc':
                if description_text != None:
                    child.text = description_text
                elif name != None:
                    child.set('name', name)
            elif child.tag == 'services':
                services = child
            elif child.tag == 'sign':
                signature = child

        #add any services directly from service object
        if services_n != None:
            for service in services_n:

                #DEBUG until a modify/update service method is created!
                counter = int(service.attrib['counter'])
                counter += 1
                counter = str(counter)
                services.set('counter', counter)

                services.append(service)

        #sign services data
        salt = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))

        raw_data = et.tostring(services).decode('utf8')

        signed_data = crypto.sign_data(raw_data, salt)

        signature.text = signed_data
        signature.set('salt', salt)

        string_xml = et.tostring(node).decode('utf8')
        return string_xml

    @staticmethod
    def __write_xml(xml_data_raw, address, node_type):
        #read index and load elements
        parser = et.XMLParser(remove_blank_text=True)
        tree = et.parse('index.xml', parser)
        root = tree.getroot()

        #overwite if element already exists (check by address)
        check = XMLIndex.get_data(node_type, address, tree)
        if check is None:
            #node does not exist
            pass
        else:
            #node exists, delete first
            root.remove(check[0])

        #convert xml string to element
        data = et.fromstring(xml_data_raw)

        root.append(data)

        tree.write('index.xml', pretty_print=True)

    @staticmethod
    def __get_xpath(address, relativepath_raw, uaddress=None):

        #relative path format example: master/services/desc
        #*[local-name()='ELEMENT_NAME_GOES_HERE'] will ignores namespace 

        root_path = '/root/'
        address_path_1 = '[address[text()=\"'
        address_path_2 = '\"]]'

        #uaddress_path_1 = '[uaddress[text()=\"'
        #uaddress_path_2 = '\"]]'

        #local_path_1 = '*[name()=\"'
        #local_path_2 = '\"]'

        #relativepath = local_path_1 + relativepath_raw + local_path_2
        relativepath = relativepath_raw

        address_path = address_path_1 + address + address_path_2

        i = relativepath.find('/', 0 , 6)

        if i == -1:
            modified_path = relativepath + address_path
        else:
            modified_path = relativepath[:i] + address_path + '/' + relativepath[i+1:]

        xpath = root_path + modified_path

        return xpath

    @staticmethod
    def get_from_uaddress(uaddress):
        uaddress_split = uaddress.split('.', 1)

        if len(uaddress_split) != 2:
            return False

        #check if node exists
        xpath = '/root/master[address[text()=\"' + uaddress_split[0] + '\"]]/services/service[desc[@name = \"' + uaddress_split[1] + '\"]]/@version'

        version_hash = XMLIndex.get_data(xpath)

        if version_hash == None:
            return False

        #create peer service node
        service = et.Element('service', version = version_hash[0])
        uaddress_el = et.SubElement(service, 'uaddress', name=uaddress_split[1])
        uaddress_el.text = uaddress_split[0]

        return service

class XMLServiceDefinition:

    @staticmethod
    def parse_xml_string(xml_data, folder_directory):

        folder_directory = folder_directory + '/'

        schema_dir= folder_directory + '.iii/iii.xsd'
        
        with open(schema_dir, 'r') as schema_file:
            schema_raw = et.XML(schema_file.read())
            schema_f = et.XMLSchema(schema_raw)

        parser = et.XMLParser(schema = schema_f, remove_comments=True, remove_blank_text=True)

        try:
            iii_root = et.fromstring(xml_data, parser)
        except:
            print('Schema validation failed!')
            return False

        #read db files and dir definitions and check if files exist as defined
        variable_files = []

        for child in iii_root:


            if child.tag == 'dbfs':
                
                files = child

                for file in files:
                    directory = folder_directory + file.text

                    exists = os.path.isfile(directory)

                    if exists:
                        variable_files.append(directory)
                    else:
                        return False

            elif child.tag == 'dbdrs':
                db_dir = child

                for dir in db_dir:
                    directory =  folder_directory +  dir.text

                    exists = os.path.isdir(directory)

                    if exists:
                        variable_files.append(directory)
                    else:
                        return False

        return variable_files

    @staticmethod
    def check_service(peer_address, service_address, service_name):
        #/root/peer[address[text()="4O5y6PUBZD6Kziz2eWo3n1TNHVTfT7x6eKwLPPUdVls="]]/services/service[uaddress[text()="O/iFe/g2ENRQfye0u0dmPd+cMUq7LoRfqmXnJt74X84="] and uaddress[@name="woot"]]/...

        #lol try reading this Xpath 
        xpath = '/root/peer[address[text()=\"' + peer_address + '\"]]/services/service[uaddress[text()=\"' + service_address + '\"] and uaddress[@name=\"' + service_name + '\"]]'
        #looking back on it, I should have just made these nice and long Xpath expressions instead of a get_xpath function

        element = XMLIndex.get_data(xpath)
        
        if element == None:
            return False

        return True

    @staticmethod
    def verify_service(service_address, service_name, service_dir):
        #/root/master[address[text()="WzJmdiSCSxk5dnT6P65UhDyNdjBnBy5E3fDxigWOHCs="]]/services/service[desc[@name = "woot"]]/data/files


        xpath = '/root/master[address[text()=\"' + service_address + '\"]]/services/service[desc[@name = \"' + service_name + '\"]]/data/files'

        #print(xpath)

        files = XMLIndex.get_data(xpath)
        service_dir = service_dir.replace('services/', '')
        glob_path = 'services\\' + service_dir + '\\**\\*'

        root_directory_raw = glob.glob(glob_path, recursive=True)
        root_directory = []

        #convert glob directories into OS friendly directories 

        for path in root_directory_raw:
            new_path = os.path.relpath(os.path.realpath(path))
            root_directory.append(new_path)

        #verify files
        remaining_p_files = root_directory
        remaining_i_files = files

        for file in files:
            if file.attrib['type'] == 'static':
                file_hash = file.text
                file_name = file.attrib['rdir']

                for p_file in root_directory:

                    if os.path.isfile(p_file):

                        p_hash = Cryptographer.generate_hash(message=None, filepath=p_file)

                        if file_hash == p_hash and file_name == p_file:
                            remaining_p_files.remove(p_file)
                            remaining_i_files.remove(file)
                    else:

                        if file_name == p_file:
                            remaining_p_files.remove(p_file)
                            remaining_i_files.remove(file)


            elif file.attrib['type'] == 'variable':
                file_name = file.attrib['rdir']

                for p_file in root_directory:
                    
                    if file_name == p_file:
                        remaining_p_files.remove(p_file)
                        remaining_i_files.remove(file)

        if len(remaining_i_files) != 0 or len(remainingremaining_p_files) != 0:
            return False

        #(Double check) Verify service version hash
        version_hash = Cryptographer.generate_hash(et.tostring(files).decode('utf8'))

        iii_version = xpath = '/root/master[address[text()=\"' + service_address + '\"]]/services/service[desc[@name = \"' + service_name + '\"]]/@version'

        if version_hash != iii_version[0]:
            return False

        return True

    @staticmethod
    def get_service_files(directory):
        directory = directory.replace('services/', '')
        glob_path = 'services\\' + directory + '\\**\\*'
        start_path = 'services/' + directory

        root_directory_raw = glob.glob(glob_path, recursive=True)

        #convert glob directories into OS friendly directories 

        root_directory = []
        for path in root_directory_raw:
            new_path = os.path.relpath(os.path.realpath(path))
            root_directory.append(new_path)

        files = et.Element('files')

        #get all variable files
        iii_xml_dir = start_path + '/.iii/iii.xml'
        with open(iii_xml_dir, 'r') as xml_file:
            db_data = xml_file.read() #maybe improve to read larger files in the future?

        variable_files_raw = XMLServiceDefinition.parse_xml_string(db_data, start_path)

        if variable_files_raw == False:

            print('[WARN] The service you have created has files that do not match with the iii.xml record')
            raise Exception('Invalid service folder')

        #normailzie paths in variable files list

        variable_files = []
        for file in variable_files_raw:
            file = os.path.normpath(file)
            variable_files.append(file)

        for p_file in root_directory:
            
            p_file = os.path.normpath(p_file)
            print(p_file)

            if p_file in variable_files:
                new_iii_path = os.path.relpath(p_file, start=start_path)
                file = et.SubElement(files, 'file', rdir=new_iii_path, type='variable')
                file.text = '0'

            elif os.path.isfile(p_file):
                p_hash = Cryptographer.generate_hash(message=None, filepath=p_file)
                new_iii_path = os.path.relpath(p_file, start=start_path)
                file = et.SubElement(files, 'file', rdir=new_iii_path, type='static')
                file.text = p_hash
            elif os.path.isdir(p_file):
                new_iii_path = os.path.relpath(p_file, start=start_path)
                file = et.SubElement(files, 'file', rdir=new_iii_path, type='static')
                file.text = '0'

        return files

    @staticmethod
    def create_new_service(files, name, desc):

        version_hash = Cryptographer.generate_hash(et.tostring(files).decode('utf8'))

        service = et.Element('service', version=version_hash, counter='0')
        description = et.SubElement(service, 'desc', name=name)
        description.text = desc

        data = et.SubElement(service, 'data')

        data.append(files)

        tags = et.SubElement(service, 'tags')

        return service




            


