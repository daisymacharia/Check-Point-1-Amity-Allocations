from Controller.amity import Amity
import unittest
import sys
from os import path


class TestDb(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()


    def test_data_successfully_exported_to_database(self):
        """ Test that data cn be loaded from the system into a database"""
            self.assertEqual('Data successfully exported to Database',
                             self.amity.save_state('data'))

    def test_data_loaded_from_database(self):
        """Test that data can be loaded into the system from a database"""
        self.assertEqual('Successfully loaded data from the Database!',
                         self.amity.load_state('data'))
