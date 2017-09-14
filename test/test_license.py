import pytest

from unittest import TestCase

from uuid import uuid4

from boalm.license import License

from boalm.hardware import get_user_name, get_mac_address, get_system_name

__author__ = 'joeny'


class LicenseTest(TestCase):

    def setUp(self):
        self.license = License()
        self.license.username = get_user_name()
        self.license.mac_address = str(get_mac_address())
        self.license.system_name = get_system_name()
        self.license.uuid = "kjqrlAp0k_GO_o_7a56gdbZrJxQHN8HlhXirmcXTJhk="
        self.license.start_date(2004, 12, 1)
        self.license.end_date(2016, 12, 1)

    def test_initial(self):
        self.assertEqual(self.license.username, 'joeny')
        self.assertEqual(self.license.mac_address, '80-86-F2-1E-E7-F3')
        self.assertEqual(self.license.system_name, 'peclt-jb')
        self.assertEqual(self.license.start, '2004-12-01')
        self.assertEqual(self.license.end, '2016-12-01')

    def test_write(self):
        self.license.write_json('output.lic')

        lic = License()
        lic.open_json('output.lic')

        self.assertEqual(lic.username, 'joeny')
        self.assertEqual(lic.mac_address, '80-86-F2-1E-E7-F3')
        self.assertEqual(lic.system_name, 'peclt-jb')
        self.assertEqual(lic.start, '2004-12-01')
        self.assertEqual(lic.end, '2016-12-01')

    def test_check_username(self):
        self.assertTrue(self.license.check_username())
        self.license.username = 'jsmith'
        self.assertFalse(self.license.check_username())

    def test_check_system_name(self):
        self.assertTrue(self.license.check_system_name())
        self.license.system_name = 'CIALAPTOP'
        self.assertFalse(self.license.check_system_name())

    def test_check_mac_address(self):
        self.assertTrue(self.license.check_mac_address())
        self.license.mac_address = '80-86-F2-1E-E7-F4'
        self.assertFalse(self.license.check_mac_address())

    def test_check_end_date(self):
        self.assertTrue(self.license.check_end_date())
        self.license.end_date(2014, 1, 01)
        self.assertFalse(self.license.check_end_date())
        self.license.end = None
        self.assertFalse(self.license.check_end_date())
