import base64
import random
import string
import os
import glob
from lxml import etree as et
from io import StringIO, BytesIO
from shutil import copyfile
from pathlib import Path
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

class XMLService:

    @staticmethod
    def generate_new_definition(name, desc, dir, type, addr):

        #create xml
        root = et.Element('def')
        
        #xml data
        service = et.SubElement(root, 'service')
        description = et.SubElement(service, 'desc')
        description.text = desc
        description.set('name', name)
        address = et.SubElement(service, 'address')
        address.text = addr
        data = et.SubElement(service, 'data')
        files = et.SubElement(data, 'files')

        #setup default files list
        root_directory = glob.glob(dir + '\\**\\*', recursive=True)

        file_list = []
        for file in root_directory:
            new_path = os.path.relpath(os.path.realpath(file))
            file_list.append(new_path)

        for file in file_list:
            if os.path.isfile(file):
            
                file_el = et.SubElement(files, 'file')
                file_el.set('rdir', os.path.relpath(file, start=dir))
                file_el.set('type', 'static')

                file_hash = Cryptographer.generate_hash(message=None, filepath=file)

                file_el.text = file_hash
            else:
                file_el = et.SubElement(files, 'file')
                file_el.set('rdir', os.path.relpath(file, start=dir))
                file_el.set('type', 'static')
                file_el.text = '0'

        depend = et.SubElement(data, 'dependencies')
        tags = et.SubElement(data, 'tags')

        if type == 'resource':
            resource = et.SubElement(tags, 'resource')
        else:
            application = et.SubElement(tags, 'application')
            application.set('os', type)
        
        version_hash = Cryptographer.generate_hash(et.tostring(data).decode('utf8'))
        service.set('version', version_hash)
        service.set('counter', '1')

        #create files

        folder = os.path.join(dir, '.iii')
        os.mkdir(folder)
        copyfile('iii.xsd', os.path.join(folder, 'iii.xsd'));


        with open(os.path.join(dir, '.iii', 'iii.xsd'), 'r') as schema_file:
            schema_raw = et.XML(schema_file.read())
            schema = et.XMLSchema(schema_raw)

        parser = et.XMLParser(schema = schema)

        #print(et.tostring(root))

        try:
            root_check = et.fromstring(et.tostring(root).decode('utf8'), parser)
        except:
            print('Schema validation failed!')
        
        tree = et.ElementTree(root)
        tree.write(os.path.join(dir, '.iii', 'iii.xml'), pretty_print=True)

    @staticmethod
    def load_definition(dir):
        iii_dir = dir + '/.iii'
        iii_xml_dir = dir + '/.iii/iii.xml'
        iii_schema_dir = dir + 'iii.xsd'

        try:
            #try opening definition and verify against schema
            
            with open(iii_schema_dir, 'r') as schema_file:
                schema_raw = et.XML(schema_file.read())
                schema_f = et.XMLSchema(schema_raw)

            parser = et.XMLParser(schema = schema_f, remove_comments=True, remove_blank_text=True)

            with open(iii_dir, 'r') as service_def:
                iii_root = et.XML(service_def.read(), parser)
            
            #get vars
            service = iii_root[0]

            static_files = []
            var_files = []

            for child in service:
                if child.tag == 'desc':
                    description = child.text
                    name = child.get('name')
                elif child.tag == 'address':
                    address = child.text
                elif child.tag == 'data':
                    version_hash = Cryptographer.generate_hash(et.tostring(child).decode('utf8'))
                    for schild in child:
                        if schild.tag == 'files':
                            xml_files = schild
                        elif schild.tag == 'dependencies':
                            dependencies = []

                            for source in schild:
                                depend = [source.get('type'), source.get('name'), source.text]
                                dependencies.append(depend)
                        elif schild.tag == 'tags':
                            tags = []

                            for tag in schild:                                
                                if tag.tag == 'application':
                                    service_type = [tag.tag, tag.get('os')]
                                    tags.append(service_type)
                                elif tag.tag == 'resource':
                                    service_type = [tag.tag]
                                    tags.append(service_type)
                                elif tag.tag == 'DELETE':
                                    delete = True
                            

            #add files to lists
            for file in xml_files:
                if file.get('type') == 'static':
                    s_file = [file.get('rdir'), file.text]
                    static_files.append(s_file)
                elif file.get('type') == 'variable':
                    v_file = file.get('rdir')
                    var_files.append(v_file)
            

            #verify file hashes and matches

            root_directory = glob.glob(iii_dir + '\\**\\*', recursive=True)

            file_list = []
            for file in root_directory:
                new_path = os.path.relpath(os.path.realpath(file))
                file_list.append(new_path)

            for file in static_files:
                if file[0] in file_list:
                    if os.path.isfile(file):
                        if file[1] == Cryptographer.generate_hash(message=None, filepath=file):
                            file_list.remove(file)
                    if os.path.isdir(file):
                            file_list.remove(file)
            var_dirs = []

            for file in var_files:
                if file in file_list:
                    if os.path.isfile(file):
                        file_list.remove(file)
                    if os.path.isdir(file):
                        var_dirs.append(file)
                        file_list.remove(file)

             #check/ignore any files in variable directory
            for file in file_list:
                for var_dir in var_dirs:
                    var_dir_path = Path(var_dir)
                    dir_path = Path(file)

                    if var_dir_path in dir_path.parents:
                        file_list.remove(file)

            if len(file_list) != 0:
                print('[ERROR] Files in service do not match service definition')
                return False

            #verify version hash
            if version_hash != service.get('version'):
                print('[ERROR] Definition version does not match data hash')
                return False

            counter = service.get('counter')

            #return service data in a list
            #dir, version, count, name, description, address, dependencies, tags [OS, type, etc], delete command
            return [dir, version_hash, counter, name, description, address, dependencies, tags, delete]

        except:
            print('[ERROR] Service defnition failed to parse (are .iii files ok?)')
            return False

    @staticmethod
    def verify_definition(dir, version, counter, name, address):
        
        version_xpath = '/root/master[address[text()=\"' + address + '\"]]/services/service[desc[@name = \"' + name + '\"]]/@version'
        counter_xpath = '/root/master[address[text()=\"' + address + '\"]]/services/service[desc[@name = \"' + name + '\"]]/@counter'
        data_xpath = '/root/master[address[text()=\"' + address + '\"]]/services/service[desc[@name = \"' + name + '\"]]/data/files'
        files = XMLIndex.get_data(data_xpath)
        index_version = XMLIndex.get_data(version_xpath)
        index_counter = XMLIndex.get_data(counter_xpath)

        if index_version[0] != version or index_counter != counter:
            return False


        static_files = []
        var_files = []

        for file in files:
            if file.get('type') == 'static':
                    s_file = [file.get('rdir'), file.text]
                    static_files.append(s_file)
            elif file.get('type') == 'variable':
                    v_file = file.get('rdir')
                    var_files.append(v_file)

        #verify file hashes and matches

        root_directory = glob.glob(dir + '\\**\\*', recursive=True)

        file_list = []
        for file in root_directory:
            new_path = os.path.relpath(os.path.realpath(file))
            file_list.append(new_path)

        for file in static_files:
            if file[0] in file_list:
                if os.path.isfile(file):
                    if file[1] == Cryptographer.generate_hash(message=None, filepath=file):
                        file_list.remove(file)
                if os.path.isdir(file):
                        file_list.remove(file)
        var_dirs = []

        for file in var_files:
            if file in file_list:
                if os.path.isfile(file):
                    file_list.remove(file)
                if os.path.isdir(file):
                    var_dirs.append(file)
                    file_list.remove(file)

        #check/ignore any files in variable directory
        for file in file_list:
            for var_dir in var_dirs:
                var_dir_path = Path(var_dir)
                dir_path = Path(file)

                if var_dir_path in dir_path.parents:
                    file_list.remove(file)

        if len(file_list) != 0:
            print('[ERROR] Files in service do not match service definition')
            return False

    @static_files
    def verify_location(address, s_address, s_name):

        xpath = '/root/peer[address[text()=\"' + address + '\"]]/services/service[uaddress[@text()=\"' + s_address + '\"] and uaddress[name = \"' + name + '\"]]'

        element = XMLIndex.get_data(xpath)
        
        if element == None:
            return False

        return True




        
             
            

                






            








        




            


