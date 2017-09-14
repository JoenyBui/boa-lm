import os
import subprocess

from unittest import TestCase

__author__ = 'joeny'


class KeyboalmApp(TestCase):

    def setUp(self):
        self.source_folder = os.path.dirname(__file__)
        self.boalm = os.path.join(os.path.split(self.source_folder)[0], 'boalm')
        self.app = os.path.join(self.boalm, 'app.py')

    def test_generate_rsa_key(self):
        self.assertFalse(subprocess.call([
            'python',
            self.app,
            'generate',
            os.path.join(self.source_folder, 'folder')
        ]))
