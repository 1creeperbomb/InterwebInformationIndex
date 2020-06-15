#Contains all key and hash methods and also handles encrypted keystore

import base64
import nacl.encoding
import nacl.signing
import nacl.utils
import nacl.secret
import nacl.hashlib
from nacl.hash import blake2b
from nacl.public import PrivateKey, Box
from nacl.encoding import Base64Encoder


class Cryptographer:
    #init
    def __init__(self, key, is_public):
        if is_public:
            #public key only, ignore private 
            public_key_clean = key

            public_key_b = base64.b64decode(public_key_clean)
            public_key = nacl.signing.VerifyKey(public_key_b)

        else:
            #private key, derive public key as well
            __private_key_clean = key

            #convert to bytes and generate object
            __private_key_b = base64.b64decode(__private_key_clean)
            __private_key = nacl.signing.SigningKey( __private_key_b)

            #generate public key
            public_key = __private_key.verify_key

    #public methods

    #private methods

    #static private methods

    #static public methods

    @staticmethod
    def generate_keypair(password):

        #converts password string to bytes sequence
        password_raw = password.encode('utf8')
    
        #generates a secret key based on the password input (blake2b will hash the person data)
        derivation_salt = nacl.utils.random(16)
        derived_key = blake2b(b'', salt=derivation_salt,
                      person=password_raw,
                      encoder=nacl.encoding.RawEncoder)

        #saves the salt to the salt.txt file
        salt_clean = base64.b64encode(derivation_salt).decode('utf8')
        with open('keystore/salt.txt', 'w') as salt_file:
            salt_file.write(salt_clean)

        #generates a keypair 
        private_key = nacl.signing.SigningKey.generate()

        #converts key to base64 format

        private_key = private_key.encode(Base64Encoder).decode('utf8')

        #encrypts the private key

        box = nacl.secret.SecretBox(derived_key)
        private_key_encrypted = box.encrypt(private_key.encode('utf8'))

        #converst to base64 again lol
        private_key_encrypted =  base64.b64encode(private_key_encrypted).decode("utf8")

        #saves the key to the keystore files

        with open('keystore/private.key', 'w') as private_file:
            private_file.write(private_key_encrypted)

    @staticmethod
    def read_key(password):
        password_raw = password.encode('utf8')

        #read private.key file
        with open('keystore/private.key', 'r') as private_file:
            private_key = private_file.read()

        #reads salt file
        with open('keystore/salt.txt', 'r') as salt_file:
            salt_clean = salt_file.read()

        #converts salt back to byte format
        derivation_salt = base64.b64decode(salt_clean)
        private_key = base64.b64decode(private_key)

        #recreates blake2b key
        derived_key = blake2b(b'', salt=derivation_salt,
                      person=password_raw,
                      encoder=nacl.encoding.RawEncoder)

        #decrypts private key
        box = nacl.secret.SecretBox(derived_key)
        private_key_decrypted = box.decrypt(private_key)

        return private_key_decrypted.decode('utf8')

    @staticmethod
    def generate_hash(filepath, message):
        hasher = nacl.hash.blake2b
        
        if filepath != 'null':
            #hash file
            with open(filepath, 'rb') as f:
                advanced_hasher = nacl.hashlib.blake2b()
                
                for chunk in iter(lambda: f.read(8192), b''):
                    advanced_hasher.update(chunk)
            
            advanced_hasher = base64.b64encode(advanced_hasher.digest()).decode('utf8')
            return advanced_hasher

        else:
            #hash string
            digest = hasher(message.encode('utf8'), encoder=nacl.encoding.Base64Encoder)
            digest = digest.decode('utf8')
            return digest



def debug():
     master_key =  nacl.utils.random(64)

     with open('keystore/salt.txt', 'r') as salt_file:
            salt_clean = salt_file.read()

     derivation_salt = base64.b64decode(salt_clean)

     password_raw = 'ya yeeet!'
     password_raw = password_raw.encode('utf8')

     derived_key = blake2b(b'', salt=derivation_salt,
                      person=password_raw,
                      encoder=nacl.encoding.RawEncoder)
     print(derived_key)

#debug run test

Cryptographer.generate_keypair("12345678")

keytest = Cryptographer.read_key("12345678")

test = Cryptographer(keytest, False)

print(Cryptographer.generate_hash('null', 'my awesome unchanging data'))

#print(Cryptographer.generate_hash('keystore/test.txt', 'null'))

#end debug run test

