import os
import sys
import json

import wx
import wx.richtext

import hardware
import keygen
from license import License
from keygen import KeyReader
from setting import Setting

__author__ = 'joeny'


class LicenseClientManager(KeyReader, License):
    """
    License Client Manager

    """
    def __init__(self):
        """
        Constructor.

        :return:
        """
        KeyReader.__init__(self)
        License.__init__(self)

        self.encrypted_file = None
        self.encrypted_key = None

        self.status = None

    def open_encrypted_file(self, filename):
        """

        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as data_file:
                self.encrypted_file = data_file.read()
        except IOError as e:
            return False
        except Exception as e:
            print(e)
            return False

        return True

    def open_encrypted_key(self, filename):
        """

        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as data_file:
                self.encrypted_key = data_file.read()
        except IOError as e:
            return False
        except Exception as e:
            print(e)
            return False

        return True

    def open_encrypted_signature(self, filename):
        """

        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as data_file:
                self.signature = data_file.read()
        except IOError as e:
            return False
        except Exception as e:
            print(e)
            return False

        return True

    def unencrypted_file(self):
        """

        :return:
        """
        if self.verified_key():

            self.hash_key = self.asymmetric_decrypt_msg(self.encrypted_key)

            key = self.symmetric_decrypt_msg(self.encrypted_file)

            self.load_data(json.loads(key))

            return True
        else:
            return False


class ClientFrame(wx.Frame):
    """
    Client wx.Frame

    """

    def __init__(self, parent, settings, icon=None, title="", message="", private_key="", public_key="", handler=None, *args, **kwargs):
        """

        :param parent:
        :param title:
        :param private_key:
        :param public_key:
        :return:
        """
        wx.Frame.__init__(self, parent, title=title, *args, **kwargs)

        self.settings = settings
        self.private_key = private_key
        self.public_key = public_key

        self.SetMinSize(wx.Size(400, 200))

        self.panel = wx.Panel(self)

        self.tb_name = wx.TextCtrl(self.panel, value=hardware.get_user_name(), style=wx.TE_READONLY)
        self.tb_system = wx.TextCtrl(self.panel, value=hardware.get_system_name(), style=wx.TE_READONLY)
        self.tb_mac = wx.TextCtrl(self.panel, value=str(hardware.get_mac_address()), style=wx.TE_READONLY)

        self.rt_info = wx.richtext.RichTextCtrl(self.panel, value=message, style=wx.VSCROLL | wx.TE_READONLY, size=(-1, 100))

        self.tb_file_path = wx.TextCtrl(self.panel, value=settings.efile, style=wx.TE_READONLY)
        self.tb_key_path = wx.TextCtrl(self.panel, value=settings.ekey, style=wx.TE_READONLY)
        self.tb_signature_path = wx.TextCtrl(self.panel, value=settings.esignature, style=wx.TE_READONLY)

        self.btn_file_path = wx.Button(self.panel, wx.ID_ANY, '', size=(24, 24))
        self.btn_key_path = wx.Button(self.panel, wx.ID_ANY, '', size=(24, 24))
        self.btn_signature_path = wx.Button(self.panel, wx.ID_ANY, '', size=(24, 24))

        self.btn_load = wx.Button(self.panel, wx.ID_ANY, 'Load File')
        self.btn_cancel = wx.Button(self.panel, wx.ID_ANY, 'Close')

        self.panel.SetSizer(self.do_layout(self.panel))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizerAndFit(sizer)

        if icon:
            self.icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.icon)

        self.bind_events()
        self.Show(True)

    def do_layout(self, panel):
        """

        :return:
        """
        label_size = (130, 24)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.do_layout_name(panel, label_size), 0, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.do_layout_system(panel, label_size), 0, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.do_layout_mac(panel, label_size), 0, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.do_layout_info(panel, label_size), 1, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.do_layout_path_file(panel, label_size), 0, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.do_layout_key_file(panel, label_size), 0, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.do_layout_signature_file(panel, label_size), 0, wx.EXPAND | wx.ALL, 0)

        sizer.Add(self.do_layout_buttons(panel), 0, wx.EXPAND | wx.ALL, 0)

        # Add Button
        return sizer

    def do_layout_name(self, panel, label_size=(150, 20)):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label="User Name", size=label_size)

        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.tb_name, 1, wx.EXPAND | wx.ALL, 5)

        return sizer

    def do_layout_system(self, panel, label_size=(150, 20)):

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label='System Name', size=label_size)

        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.tb_system, 1, wx.EXPAND | wx.ALL, 5)

        return sizer

    def do_layout_mac(self, panel, label_size=(150, 20)):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label="MAC", size=label_size)

        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.tb_mac, 1, wx.EXPAND | wx.ALL, 5)

        return sizer

    def do_layout_info(self, panel, label_size=(150, 20)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Info")
        sizer = wx.StaticBoxSizer(box_keys, wx.VERTICAL)

        sizer.Add(self.rt_info, 1, wx.ALL | wx.EXPAND, 0)

        return sizer

    def do_layout_path_file(self, panel, label_size=(150, 20)):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label="Encrypted File", size=label_size)

        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.tb_file_path, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_file_path, 0, wx.EXPAND | wx.ALL, 5)

        return sizer

    def do_layout_key_file(self, panel, label_size=(150, 20)):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label="Encrypted Key Path", size=label_size)

        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.tb_key_path, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_key_path, 0, wx.EXPAND | wx.ALL, 5)

        return sizer

    def do_layout_signature_file(self, panel, label_size=(150, 20)):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label="Signature Path", size=label_size)

        sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.tb_signature_path, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.btn_signature_path, 0, wx.EXPAND | wx.ALL, 5)

        return sizer

    def do_layout_buttons(self, panel):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(self.btn_load, 1, wx.EXPAND | wx.ALL, 5)
        sizer.AddSpacer(5)
        sizer.Add(self.btn_cancel, 1, wx.EXPAND | wx.ALL, 5)

        return sizer

    def bind_events(self):
        """
        Bind events.

        :return:
        """
        self.btn_file_path.Bind(wx.EVT_BUTTON, self.click_encrypted_file)
        self.btn_key_path.Bind(wx.EVT_BUTTON, self.click_encrypted_key)
        self.btn_signature_path.Bind(wx.EVT_BUTTON, self.click_encrypted_signature)

        self.btn_load.Bind(wx.EVT_BUTTON, self.click_load_license)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.click_cancel)

    def click_encrypted_file(self, event):
        """
        Find encrypted file path.

        :param event:
        :return:
        """
        path, file = os.path.split(self.settings.efile)

        if os.path.isdir(path):
            dlg = wx.FileDialog(self, defaultDir=path)
        else:
            dlg = wx.FileDialog(self)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            self.tb_file_path.Value = path

    def click_encrypted_key(self, event):
        """
        Find encrypted key path.

        :param event:
        :return:
        """
        path, file = os.path.split(self.settings.ekey)

        if os.path.isdir(path):
            dlg = wx.FileDialog(self, defaultDir=path)
        else:
            dlg = wx.FileDialog(self)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            self.tb_key_path.Value = path

    def click_encrypted_signature(self, event):
        """
        File encrypted signature path.

        :param event:
        :return:
        """
        path, file = os.path.split(self.settings.esignature)

        if os.path.isdir(path):
            dlg = wx.FileDialog(self, defaultDir=path)
        else:
            dlg = wx.FileDialog(self)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            self.tb_signature_path.Value = path

    def click_load_license(self, event):
        valid = True

        if os.path.isfile(self.tb_file_path.Value):
            self.settings.efile = self.tb_file_path.Value

        if os.path.isfile(self.tb_key_path.Value):
            self.settings.ekey = self.tb_key_path.Value

        if os.path.isfile(self.tb_signature_path.Value):
            self.settings.esignature = self.tb_signature_path.Value

        if valid:
            self.settings.save_to_settings()

            self.Close()
        else:
            wx.MsgBox("Some files does not exists")

    def click_cancel(self, event):
        exit()

if __name__ == '__main__':
    frozen = 'not'

    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environement
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    print('we are ', frozen, 'frozen')
    print('bundle dir is', bundle_dir)
    print('file', __file__)
    print('sys.arg[0] is', sys.argv[0])
    print('sys.executable is ', sys.executable)
    print('os.getcwd is', os.getcwd())

    # Start Frame.
    message = "Please contact joeny@protection-consultants and provide the following information."

    settings = Setting()
    settings.ekey=""
    settings.efile=""
    settings.esignature=""

    app = wx.App(False)
    frame = ClientFrame(None,
                        settings,
                        "Small Editor",
                        message=message,
                        size=(400, 400))
    app.MainLoop()

