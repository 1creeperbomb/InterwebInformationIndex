import base64
from lxml import etree as et
from io import StringIO, BytesIO
from main_package.cryptographer import Cryptographer

class Xml_index:
    #init

    #methods
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

        for child in root:
            if child.tag == 'address':
                address = child.text
            elif child.tag == 'sign':
                signature = child.text
            elif child.tag == 'services':
                data = et.tostring(child).decode('utf8')

        try:
            crypto = Cryptographer(address, True)
            if crypto.verify_data(data, signature):
                print('Signature verified successfully!')
            else:
                print('Signature failed to verify')
                return False;
        except:
            print('Invalid key / key is corrupt')
            return False;

        #send data to write method and socket sever
        write_xml(xml_data_raw)

        return True

    def write_xml(xml_data_raw):
        #read index and load elements
        tree = et.parse('index.xml')
        root = tree.getroot()

        #convert xml string to element
        data = et.fromstring(xml_data_raw)

        root.append(data)

        tree.write('index.xml')
