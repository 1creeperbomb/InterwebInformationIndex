#debug file to test classes and import
from main_package.cryptographer import Cryptographer
from main_package.xml import Xml_index



#Cryptographer.generate_keypair('test password')
private_key = Cryptographer.read_key('test password')

crypto = Cryptographer(private_key, False)

print('private key: ' + private_key)

data_test = '<services><service version="+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs="><desc name="woot">ya man</desc><data><files><file rdir="assets/pic.img" type="static">+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs=</file></files></data></service></services>'
signed = crypto.sign_data(data_test)

print(signed)

verified = crypto.verify_data(data_test, signed)

print(verified)

#print(Xml_index.get_data('4O5y6PUBZD6Kziz2eWo3n1TNHVTfT7x6eKwLPPUdVls=', 'peer'))

Xml_index.parse_xml_string('<master><address>WzJmdiSCSxk5dnT6P65UhDyNdjBnBy5E3fDxigWOHCs=</address><sign salt="1234567890123456">ptNtqdUn/MtpoHFLgcodcYaD9DAmV3xVRI9+/K7pZGYIccNd61KC4LrIZz+bEhznR+f3p/hXWK7jWD/jzPdXCw==</sign><desc name="my master node">my EVEN cool master node</desc><services><service version="+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs="><desc name="woot">ya man</desc><data><files><file rdir="assets/pic.img" type="static">+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs=</file></files></data></service></services></master>')

#<services><service version="+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs="><desc name="woot">ya man</desc><data><files><file rdir="assets/pic.img" type="static">+/R0wiWAKlUmwqA2XjdYfspZ8Gu7StXKSc1u+C2naAs=</file></files></data></service></services>