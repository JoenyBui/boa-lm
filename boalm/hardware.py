import os
import sys
import platform
import socket
import getpass

from uuid import getnode

import netaddr

__author__ = 'joeny'


def get_mac_address():
    """
    Return the MAC address.

    :return:
    """
    mac = getnode()

    return netaddr.EUI(mac)


def get_system_name():
    """
    Return the system name.

    :return:
    """
    return socket.gethostname()


def get_user_name():
    """
    Return the user name.

    :return:
    """
    return getpass.getuser()


def get_os():
    """
    Return operating system.

    :return:
    """
    return platform.platform()


def get_version():
    """
    Return the version.

    :return:
    """
    return platform.version()


def get_machine():
    """
    Return the machine.

    :return:
    """
    return platform.machine()
