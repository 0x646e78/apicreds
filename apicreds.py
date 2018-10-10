#!/usr/bin/python

# yeah, so my refactoring has started, and so this is presently pretty ugly - but it works!

import sys
import argparse
import yaml
import os
from getpass import getpass
from simplecrypt import encrypt, decrypt

# Set options
default_keyfile = "~/.apicreds.aes"

class LocalFile:
    """Encrypt creds in a local AES file"""
    def __init__(self, action, keyfile):
        self.filename = keyfile
        if not os.path.exists(keyfile):
            if 'insert' in action:
                sys.stderr.write(str("Key file %s does not exist. Would you like to create a new keyfile?\ny/n (n): " % keyfile))
                decision = raw_input()
                if decision.lower() in ['y', 'yes']:
                    self.passwd = getpass('Enter a passphrase to protect your key file> ')
                else:
                    exit(1)
            else:
                print "Keyfile %s does not exist" % args.keyfile
                exit(1)
        else:
            with open(keyfile, 'r') as file:
                encrypted_file = file.read()
                count =0
                while count < 3:
                    self.passwd = getpass('Enter your passphrase> ')
                    try:
                        self.keyfile = self.decryptor(encrypted_file)
                        return
                    except Exception as e:
                        print "Incorrect passphrase, please try again", e
                        count = count + 1
                else:
                    exit(0)

    def decryptor(self, text):
        decrypted = decrypt(self.passwd, text)
        return decrypted

    def encryptor(self, text):
        encrypted = encrypt(self.passwd, text)
        with open(self.filename, 'w') as file:
            file.write(encrypted)
        os.chmod(self.filename, 0600)

 
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='apicreds.py - Manage API keys')
    parser.add_argument('-f','--keyfile', help='The keyfile to use', default=os.path.expanduser(default_keyfile))
    parser.add_argument('-e','--env', help='The environment name to source, i.e prod-work')
    parser.add_argument('-i','--insert', help='Insert a new credential set', action="store_true")
    parser.add_argument('-l','--list', help='List stored environments', action="store_true")
    parser.add_argument('-u','--update', help='Update a stored environment', action="store_true")
    parser.add_argument('-d','--delete', help='Delete stored environments', nargs='?', const='none')
    parser.add_argument('--new-passphrase', help='Update the storage passphrase', action="store_true")
    parser.add_argument('-v','--verbose', help='Increase verbosity', action="store_true")
    args = parser.parse_args()

    # Check for required CLI options
    if not args.insert and not args.list and not args.env and not args.delete and not args.update:
        parser.error('Incorrect arguments provided.\n\nUse --help for detailed help.')

    if not os.path.exists(args.keyfile):
        if args.insert:
            localfile = LocalFile('insert', args.keyfile)
        else:
            print "File %s does not exist. Exiting." % args.keyfile
            sys.exit(1)
    else:
        localfile = LocalFile('read', args.keyfile)
        keyfile = localfile.keyfile

    if args.update:
        print "Update not yet impletemted. Please come again."
        sys.exit(0)
    elif args.insert:
        if not args.env:
            sys.stderr.write(str("\nEnter the name of your new API environment: "))
            apienv = raw_input()
        else:
            apienv = args.env

        if 'keyfile' in locals():
            keys = yaml.load(keyfile)
        else:
            keys = {}

        if apienv in keys:
            sys.stderr.write(str("The specified environment already exists.  Do you wish to overwrite these credentials?i\ny/n (n): "))
            overwrite = raw_input()
            if overwrite.lower() in ['n', 'no']:
                return(0)

        sys.stderr.write(str("\nEnter a brief desciption of the environment: "))
        awsdesc = raw_input()
        sys.stderr.write(str("\nEnter your AWS Access Key ID: "))
        awsid = raw_input()
        awspass = getpass("Enter your AWS Secret Key: ")
        sys.stderr.write(str("\nEnter the default region for this environment (blank for none): "))
        awsregion = raw_input()

        keys[apienv] = {"provider": "aws", "description": awsdesc, "id": awsid, "secret": awspass, "region": awsregion} 
        keyfile = yaml.dump(keys)
        localfile.encryptor(keyfile)
    elif args.delete:
        if args.delete is 'none':
            sys.stderr.write(str("\nEnter the name of the API environment to delete: "))
            apienv = raw_input()
        else:
            apienv = args.delete

        keys = yaml.load(keyfile)

        if apienv not in keys:
            print "%s not found in credential set" % apienv
        else:
            sys.stderr.write(str("\nAre you sure you want to delete environment '%s'?\ny/n (n): " % apienv))
            delete = raw_input()
            if delete.lower() in ['n', 'no']:
                return(0)

        del(keys[apienv])
        keyfile = yaml.dump(keys)
        localfile.encryptor(keyfile)
    else:
        with open (os.path.join(os.path.dirname(__file__), 'providers.yaml'), 'r') as f:
            providers = yaml.load(f)
        keys = yaml.load(localfile.keyfile)
        if args.list:
            for key in keys:
                if args.env and not key in args.env:
                    continue
                print '\nEnvironment: ', key
                for element,value in providers['providers']['aws'].items():
                    if keys[key][element] and element != 'secret':
                        print value['describe'], ':',  keys[key][element]
        else:
            for element,value in providers['providers']['aws'].items():
                if value['env']:
                    print "export %s=%s" % (value['env'], keys[args.env][element])
    
if __name__ == "__main__":
    main()
