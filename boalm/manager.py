from datetime import datetime
from datetime import date

import os
import json
import uuid

import wx
import wx.calendar
import wx.richtext

import hardware

from license import License
from keygen import KeyGenerator

__author__ = 'joeny'


class LicensePublisherManager(KeyGenerator, License):
    """
    License Publisher Manager

    """

    def __init__(self):
        """
        Constructor.

        """
        KeyGenerator.__init__(self)
        License.__init__(self)

        self.encrypted_file = None
        self.encrypted_key = None

    def encrypt_file(self):
        """
        Encrypt file.

        """

        lic = self.write_data()

        self.encrypted_file = self.symmetric_encrypt_msg(json.dumps(lic))
        self.encrypted_key = self.asymmetric_encrypt_msg(self.hash_key)

    def write_encrypt_file(self, filename='FILE'):
        """
        Write encrypted file.

        :param filename:
        """
        if self.encrypted_file:
            with open(filename, 'wb') as data_file:
                data_file.write(self.encrypted_file)
        else:
            print("No Encrypted File.")

    def write_encrypt_key(self, keyname='KEY'):
        """
        Write encrypted key.

        :param keyname:
        """
        if self.encrypted_key:
            with open(keyname, 'wb') as data_file:
                data_file.write(self.encrypted_key)
        else:
            print('No Encrypted Key')

    def write_signature(self, filename='SIGNATURE'):
        """
        Write signature file.

        :param filename:
        """
        if self.signature:
            with open(filename, 'wb') as data_file:
                data_file.write(self.signature)
        else:
            print('No Signature')


class ManagerFrame(wx.Frame):
    """
    Manager wx.Frame

    """
    def __init__(self, parent, title, uuid='12002', hash_key='12345', public_key="public", private_key="private", size=(300, 200)):
        wx.Frame.__init__(self, parent, title=title, size=size)

        textbox_size = (150, 20)

        today = datetime.today().date()

        year, month, day = tuple(str(today).split('-'))

        self.license = LicensePublisherManager()

        self.panel = wx.Panel(self)

        self.tb_name = wx.TextCtrl(self.panel, value=hardware.get_user_name(), size=textbox_size)
        self.tb_system = wx.TextCtrl(self.panel, value=hardware.get_system_name(), size=textbox_size)
        self.tb_mac = wx.TextCtrl(self.panel, value=str(hardware.get_mac_address()), size=textbox_size)
        self.tb_uuid = wx.TextCtrl(self.panel, value=str(uuid), size=textbox_size, style=wx.TE_READONLY)

        self.tb_year = wx.TextCtrl(self.panel, value=year, size=textbox_size)
        self.tb_month = wx.TextCtrl(self.panel, value=month, size=textbox_size)
        self.tb_day = wx.TextCtrl(self.panel, value=day, size=textbox_size)

        self.calendar = wx.calendar.CalendarCtrl(self.panel, -1, wx.DateTime_Now(), pos=(25, 50),
                                                 style=wx.calendar.CAL_SHOW_HOLIDAYS |
                                                       wx.calendar.CAL_SUNDAY_FIRST |
                                                       wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION
                                                 )

        self.tb_path = wx.TextCtrl(self.panel, id=wx.ID_ANY, size=(240, 24), value=os.getcwd(), style=wx.TE_READONLY)
        self.btn_path = wx.Button(self.panel, id=wx.ID_ANY, size=(24, 24))

        self.btn_generate = wx.Button(self.panel, id=wx.ID_ANY, label='Generate', size=(280, 30))
        self.btn_close = wx.Button(self.panel, id=wx.ID_ANY, label='Close', size=(280, 30))

        self.tb_hash_key = wx.TextCtrl(self.panel, value=hash_key, size=(490, 20), style=wx.TE_READONLY)

        self.rb_private_key = wx.richtext.RichTextCtrl(self.panel, size=(490, 300), style=wx.VSCROLL | wx.TE_READONLY)
        self.rb_private_key.AppendText(private_key)

        self.rb_public_key = wx.richtext.RichTextCtrl(self.panel, size=(490, 200), style=wx.VSCROLL | wx.TE_READONLY)
        self.rb_public_key.AppendText(public_key)

        self.panel.SetSizer(self.do_layout(self.panel))
        self.panel.Layout()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizerAndFit(sizer)

        self.bind_methods()
        self.Show()

    def bind_methods(self):
        self.Bind(wx.calendar.EVT_CALENDAR, self.on_calendar_selected, id=self.calendar.GetId())
        self.Bind(wx.calendar.EVT_CALENDAR_MONTH, self.on_change_month, self.calendar)
        self.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.on_calendar_selected_change, id=self.calendar.GetId())

        self.btn_path.Bind(wx.EVT_BUTTON, self.on_click_path)
        self.btn_generate.Bind(wx.EVT_BUTTON, self.on_click_generate)
        self.btn_close.Bind(wx.EVT_BUTTON, self.on_click_close)

    def do_layout(self, panel):
        """
        Do layout.

        :return:
        """
        int_margin = 10
        label_size = (150, 20)
        box_size = (310, 30)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        vs1 = wx.BoxSizer(wx.VERTICAL)

        vs1.AddSpacer(int_margin)
        vs1.Add(self.do_layout_key(panel, int_margin=int_margin, label_size=label_size, box_size=box_size), 0, wx.ALL | wx.CENTER, 2)
        vs1.AddSpacer(int_margin)
        vs1.Add(self.do_layout_exp_date(panel, int_margin=int_margin, label_size=label_size, box_size=box_size), 0, wx.ALL | wx.CENTER, 2)
        vs1.AddSpacer(int_margin)
        vs1.Add(self.do_layout_path(panel, int_margin=int_margin, label_size=label_size, box_size=box_size), 0, wx.ALL | wx.CENTER, 2)
        vs1.AddStretchSpacer(1)
        vs1.Add(self.btn_generate, 0, wx.ALL | wx.CENTER, 2)
        vs1.AddSpacer(int_margin)
        vs1.Add(self.btn_close, 0, wx.ALL | wx.CENTER, 0)
        vs1.AddSpacer(int_margin)

        vs2 = wx.BoxSizer(wx.VERTICAL)
        vs2.Add(self.do_layout_hash_key(panel, int_margin=int_margin, label_size=label_size, box_size=box_size), 0, wx.ALL | wx.EXPAND, 2)
        vs2.AddSpacer(int_margin)
        vs2.Add(self.do_layout_private_key(panel, int_margin=int_margin, label_size=label_size, box_size=box_size), 1, wx.ALL | wx.EXPAND, 2)
        vs2.AddSpacer(int_margin)
        vs2.Add(self.do_layout_public_key(panel, int_margin=int_margin, label_size=label_size, box_size=box_size), 1, wx.ALL | wx.EXPAND, 2)
        vs2.AddSpacer(int_margin)

        sizer.Add(vs1, 0, wx.ALL | wx.EXPAND, 0)
        sizer.Add(vs2, 1, wx.ALL | wx.EXPAND, 0)

        return sizer

    def do_layout_path(self, panel, int_margin=10, label_size=(150, 20), box_size=(240, 140)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Keys", size=box_size)
        sizer = wx.StaticBoxSizer(box_keys, wx.HORIZONTAL)

        sizer.AddSpacer(int_margin)
        sizer.Add(self.tb_path, 0, wx.ALL | wx.CENTER, 0)
        sizer.AddSpacer(int_margin)
        sizer.Add(self.btn_path, 0, wx.ALL | wx.CENTER, 0)

        return sizer

    def do_layout_key(self, panel, int_margin=10, label_size=(150, 20), box_size=(240, 140)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Keys", size=box_size)
        sizer = wx.StaticBoxSizer(box_keys, wx.VERTICAL)
        sizer.AddSpacer(int_margin)

        # MAC Address
        lb_mac = wx.StaticText(panel, label="Hardware MAC", size=label_size)
        sz_mac = wx.BoxSizer(wx.HORIZONTAL)
        sz_mac.Add(lb_mac)
        sz_mac.Add(self.tb_mac)

        sizer.Add(sz_mac, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        # System Name
        lb_system = wx.StaticText(panel, label="System Name", size=label_size)
        sz_system = wx.BoxSizer(wx.HORIZONTAL)
        sz_system.Add(lb_system)
        sz_system.Add(self.tb_system)
        sizer.Add(sz_system, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        # Name
        lb_name = wx.StaticText(panel, label="User Name", size=label_size)
        sz_name = wx.BoxSizer(wx.HORIZONTAL)
        sz_name.Add(lb_name)
        sz_name.Add(self.tb_name)
        sizer.Add(sz_name, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        # UUID
        lb_uuid = wx.StaticText(panel, label='UUID', size=label_size)
        sz_uuid = wx.BoxSizer(wx.HORIZONTAL)
        sz_uuid.Add(lb_uuid)
        sz_uuid.Add(self.tb_uuid)
        sizer.Add(sz_uuid, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        return sizer

    def do_layout_exp_date(self, panel, int_margin=10, label_size=(150, 20), box_size=(240, 140)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Expiration Date", size=box_size)
        sizer = wx.StaticBoxSizer(box_keys, wx.VERTICAL)
        sizer.AddSpacer(int_margin)

        # Year
        lb_year = wx.StaticText(panel, label="Year", size=label_size)
        sz_year = wx.BoxSizer(wx.HORIZONTAL)
        sz_year.Add(lb_year)
        sz_year.Add(self.tb_year)

        sizer.Add(sz_year, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        # Month
        lb_month = wx.StaticText(panel, label="Month", size=label_size)
        sz_month = wx.BoxSizer(wx.HORIZONTAL)
        sz_month.Add(lb_month)
        sz_month.Add(self.tb_month)
        sizer.Add(sz_month, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        # Day
        lb_day = wx.StaticText(panel, label="Day", size=label_size)
        sz_day = wx.BoxSizer(wx.HORIZONTAL)
        sz_day.Add(lb_day)
        sz_day.Add(self.tb_day)
        sizer.Add(sz_day, 0, wx.ALL | wx.CENTER, 2)
        sizer.AddSpacer(int_margin)

        sizer.AddSpacer(int_margin)
        sizer.Add(self.calendar, 0, wx.ALL | wx.CENTER, 2)

        return sizer

    def do_layout_hash_key(self, panel, int_margin=10, label_size=(150, 20), box_size=(240, 140)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Hash Key", size=box_size)
        sizer = wx.StaticBoxSizer(box_keys, wx.VERTICAL)
        sizer.AddSpacer(int_margin)

        sizer.Add(self.tb_hash_key, 1, wx.ALL | wx.EXPAND, 0)

        return sizer

    def do_layout_private_key(self, panel, int_margin=10, label_size=(150, 20), box_size=(240, 140)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Private Key", size=box_size)
        sizer = wx.StaticBoxSizer(box_keys, wx.VERTICAL)
        sizer.AddSpacer(int_margin)

        sizer.Add(self.rb_private_key, 1, wx.ALL | wx.EXPAND, 0)

        return sizer

    def do_layout_public_key(self, panel, int_margin=10, label_size=(150, 20), box_size=(240, 140)):
        box_keys = wx.StaticBox(panel, wx.ID_ANY, "Public Key", size=box_size)
        sizer = wx.StaticBoxSizer(box_keys, wx.VERTICAL)
        sizer.AddSpacer(int_margin)

        sizer.Add(self.rb_public_key, 1, wx.ALL | wx.EXPAND, 0)

        return sizer

    def on_calendar_selected(self, event=None):
        print('on_calendar_selected')

    def on_change_month(self, event=None):
        print('on_change_month')

    def on_calendar_selected_change(self, event=None):
        print('on_calendar_selected_change')

        select_date = self.calendar.GetDate()
        year = select_date.GetYear()
        month = select_date.GetMonth()
        day = select_date.GetDay()

        self.tb_year.SetValue(unicode(year))
        self.tb_month.SetValue(unicode(month))
        self.tb_day.SetValue(unicode(day))

    def on_click_path(self, event=None):
        dlg = wx.DirDialog(self)

        if dlg.ShowModal():
            path = dlg.GetPath()

            if os.path.isdir(path):
                self.tb_path.SetValue(dlg.GetPath())

        dlg.Destroy()

    def on_click_generate(self, event=None):
        print('on_click_generate')

        path = self.tb_path.GetValue()

        if os.path.isdir(path):
            self.license.username = self.tb_name.GetValue()
            self.license.mac_address = self.tb_mac.GetValue()
            self.license.system_name = self.tb_system.GetValue()
            self.license.end_date(self.tb_year.GetValue(), self.tb_month.GetValue(), self.tb_day.GetValue())
            self.license.uuid = self.tb_uuid.GetValue()

            self.license.load_private_key(str(self.rb_private_key.GetValue()))
            self.license.load_public_key(str(self.rb_public_key.GetValue()))
            self.license.hash_key = str(self.tb_hash_key.GetValue())
            self.license.encrypt_file()
            self.license.sign_key()

            self.license.write_encrypt_file(os.path.join(path, 'FILE'))
            self.license.write_encrypt_key(os.path.join(path, 'KEY'))
            self.license.write_signature(os.path.join(path, 'SIGNATURE'))
        else:
            wx.MessageBox("Path does not exists.")

    def on_click_close(self, event=None):
        self.Close()

if __name__ == '__main__':
    from cryptography.fernet import Fernet

    kg = KeyGenerator()
    kg.generate_rsa_key()

    hash_key = Fernet.generate_key()
    (pubkey, privkey) = kg.public_key(), kg.private_key()

    kg.generate_rsa_key()
    (rpubkey, rprivkey) = kg.public_key(), kg.private_key()

    app = wx.App(False)
    frame = ManagerFrame(None,
                         "License Generator Manager",
                         hash_key=hash_key,
                         uuid=str(uuid.uuid4()),
                         public_key=pubkey,
                         private_key=privkey,
                         size=(400, 600))
    app.MainLoop()
