from amity.Controller.amity import Amity
import unittest
from io import StringIO
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestDb(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()


    def test_data_successfully_exported_to_database(self):
        """ Test that data can be loaded from the system into a database"""
        self.amity.save_state('data')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Data successfully exported to Database', message)

    def test_data_loaded_from_database(self):
        """Test that data can be loaded into the system from a database"""
        self.amity.load_state('data')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Successfully loaded data from the Database.', message)
