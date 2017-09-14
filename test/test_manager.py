from unittest import TestCase

from boalm.license import License
from boalm.hardware import get_user_name, get_mac_address, get_system_name
from boalm.manager import LicenseClientManager, LicensePublisherManager

from cryptography.exceptions import InvalidSignature

__author__ = 'joeny'


class PublisherManagerTest(TestCase):

    def setUp(self):
        self.pub = LicensePublisherManager()
        self.pub.open_private_key('gen_private.key')
        self.pub.open_public_key('reader_public.key')
        self.pub.hash_key = "kjqrlAp0k_GO_o_7a56gdbZrJxQHN8HlhXirmcXTJhk="
        self.pub.open_json('output.lic')

        self.pub.encrypt_file()
        self.pub.sign_key()

    def test_encrypt_file(self):
        self.pub.write_encrypt_file('FILE')
        self.pub.write_encrypt_key('KEY')
        self.pub.write_signature('SIGNATURE')


class ClientManagerTest(TestCase):

    def setUp(self):
        self.client = LicenseClientManager()
        self.client.open_private_key('reader_private.key')
        self.client.open_public_key('gen_public.key')

    def test_load_license_file(self):
        self.client.open_encrypted_file('FILE')
        self.client.open_encrypted_key('KEY')
        self.client.open_encrypted_signature('SIGNATURE')
        self.client.unencrypted_file()

        self.assertEqual(self.client.username, 'joeny')
        self.assertEqual(self.client.mac_address, '80-86-F2-1E-E7-F3')
        self.assertEqual(self.client.system_name, 'peclt-jb')
        self.assertEqual(self.client.start, '2004-12-01')
        self.assertEqual(self.client.end, '2016-12-01')
        self.assertEqual(self.client.uuid, "2ab158e2-1c23-474b-bd42-aaaa07b77341")

    def test_bad_signature(self):
        self.client.open_encrypted_file('FILE')
        self.client.open_encrypted_key('KEY')
        self.client.open_encrypted_signature('BAD_SIGNATURE')

        self.assertFalse(self.client.unencrypted_file())

