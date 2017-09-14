#!/usr/bin/python
"""
Usage: lm
    lm open <FILE>
    lm hash <FOLDER>
    lm generate <FOLDER>
    lm uuid <FOLDER>
    lm system <FOLDER>

Arguments:
    FILE            input file
    FOLDER          output folder
"""

from __future__ import absolute_import

import os
import sys
import logging

from docopt import docopt

__version__ = 0.1
__author__ = 'joeny'

# Get an instance of a logger.
logger = logging.getLogger(__name__)


if __name__ == '__main__' and __package__ is None:
    # Relative Import Hack
    package_name = 'boalm'
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(1, parent_dir)
    mod = __import__(package_name)
    sys.modules[package_name] = mod
    __package__ = package_name

    from .keygen import KeyGenerator

    arguments = docopt(__doc__)

    current_directory = os.getcwd()

    try:
        if arguments.get('generate'):
            kg = KeyGenerator()
            kg.generate_rsa_key()

            (pubkey, privkay) = kg.public_key(), kg.private_key()

            folder = arguments.get('<FOLDER>')

            print('=== Public Key ===')
            print(pubkey)
            if pubkey:
                with open(os.path.join(folder, 'key.cert'), 'w') as data_file:
                    data_file.write(pubkey)

            print('=== Private Key ===')
            print(privkay)
            if privkay:
                with open(os.path.join(folder, 'key.pem'), 'w') as data_file:
                    data_file.write(privkay)

        elif arguments.get('hash'):
            from cryptography.fernet import Fernet

            folder = arguments.get('<FOLDER>')

            hash_key = Fernet.generate_key()

            print(hash_key)
            if hash_key:
                with open(os.path.join(folder, 'hash.key'), 'w') as data_file:
                    data_file.write(hash_key)

        elif arguments.get('uuid'):
            import uuid

            folder = arguments.get('<FOLDER>')

            value = str(uuid.uuid4())
            if value:
                with open(os.path.join(folder, 'uuid.key'), 'w') as data_file:
                    data_file.write(value)

        elif arguments.get('system'):
            from .hardware import get_mac_address, get_system_name, get_user_name

            print('MAC')
            print(get_mac_address())

            print('SYSTEM')
            print(get_system_name())

            print('USERNAME')
            print(get_user_name())

    except Exception as e:
        print(e)

    finally:
        os.chdir(current_directory)
