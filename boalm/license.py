import os
import time

from datetime import datetime, date

import json

from uuid import uuid4

from hardware import get_user_name, get_mac_address, get_system_name

__author__ = 'joeny'


class License(object):
    """
    Generate a license file.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.

        :param args:
        :param kwargs:
        :return:
        """
        self.username = kwargs.get('username', None)
        self.mac_address = kwargs.get('mac_address', None)
        self.system_name = kwargs.get('system_name', None)
        self.uuid = kwargs.get('uuid', None)
        self.start = kwargs.get('start', None)
        self.end = kwargs.get('end', None)

    def system_info(self):
        """
        System Information.

        :return:
        """
        self.username = get_user_name()
        self.mac_address = get_mac_address()
        self.system_name = get_system_name()

    def check_username(self):
        """
        Check username.

        :return:
        """
        if self.username == get_user_name():
            return True
        else:
            return False

    def check_system_name(self):
        """
        Check system name.

        :return:
        """
        if self.system_name == get_system_name():
            return True
        else:
            return False

    def check_mac_address(self):
        """
        Check MAC address.

        :return:
        """
        if self.mac_address == get_mac_address():
            return True
        else:
            return False

    def check_end_date(self):
        """
        Check end date.

        :return:
        """
        if self.end is None:
            return False

        exp = datetime.strptime(self.end, '%Y-%m-%d')

        today = datetime.today()

        if exp < today:
            return False
        else:
            return True

    def write_data(self):
        """
        Write data.

        :return:
        """
        key = dict(
            username=self.username,
            mac_address=self.mac_address,
            system_name=self.system_name,
            uuid=self.uuid,
            start=self.start,
            end=self.end
        )

        return key

    def write_json(self, filename=''):
        """
        Write JSON data.

        :param filename:
        :return:
        """
        data = self.write_data()

        with open(filename, 'w') as datafile:
            json.dump(data, datafile, indent=4, sort_keys=True)

    def load_data(self, key):
        """
        Load the key date.

        :param key:
        :return:
        """
        self.username = key.get('username')
        self.mac_address = key.get('mac_address')
        self.system_name = key.get('system_name')
        self.uuid = key.get('uuid')
        self.start = key.get('start')
        self.end = key.get('end')

    def open_json(self, filepath):
        """
        Open JSON.

        :param filepath:
        :return:
        """
        if os.path.join(filepath):
            with open(filepath, 'r') as datafile:
                self.load_data(json.loads(datafile.read()))

    def start_date(self, year, month, day):
        """
        Start Date.

        :param year:
        :param month:
        :param day:
        :return:
        """
        self.start = str(date(year, month, day))

    def end_date(self, year, month, day):
        """
        End Date.

        :param year:
        :param month:
        :param day:
        :return:
        """
        self.end = str(date(int(year), int(month), int(day)))

