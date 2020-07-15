import base64
import random
import string
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

        node_type = root.tag

        for child in root:
            if child.tag == 'address':
                address = child.text
            elif child.tag == 'sign':
                signature = child.text
                salt = child.attrib['salt']
            elif child.tag == 'services':
                data = et.tostring(child).decode('utf8')

        try:
            crypto = Cryptographer(address, True)
            if crypto.verify_data(data, signature, salt):
                print('Signature verified successfully!')
            else:
                print('Signature failed to verify')
                return False;
        except:
            print('Invalid key / key is corrupt')
            return False;

        #send data to write method and socket sever
        XMLIndex.__write_xml(xml_data_raw, address, node_type)

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
        data = tree.xpath(xpath)

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

        #sign services data
        raw_data = et.tostring(services).decode('utf8')

        signed_data = crypto.sign_data(raw_data, salt)

        signature.text = signed_data

        string_xml = et.tostring(root).decode('utf8')

        return string_xml

    def modify_node(type, crypto, address, name=None, description_text=None):
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
                salt = child.attrib['salt']

        #add statement for services in the future


        #sign services data

        raw_data = et.tostring(services).decode('utf8')

        signed_data = crypto.sign_data(raw_data, salt)

        signature.text = signed_data

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
    def __get_xpath(address, relativepath_raw):

        #relative path format example: master/services/desc
        #*[local-name()='ELEMENT_NAME_GOES_HERE'] will ignores namespace 

        root_path = '/root/'
        address_path_1 = '[address[text()=\"'
        address_path_2 = '\"]]'

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









