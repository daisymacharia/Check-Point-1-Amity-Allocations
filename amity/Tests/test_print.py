from io import StringIO
from amity.Controller.amity import Amity
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestPeople(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()
        self.amity.all_rooms = {'livingspace': [], 'office': []}
        self.amity.waiting_list = {'office': [], 'livingspace': []}
        self.amity.all_people = {'staff': [], 'fellow': []}

    def test_print_room(self):
        """Tests that the room occupants in a room are printed"""
        self.amity.create_room('OFFICE', 'test_office')
        self.amity.add_person('FELLOW', 'Wanjiru', 'N')
        self.amity.print_room("test_office")
        message = sys.stdout.getvalue().strip()
        self.assertIn("Wanjiru", message)

    def test_print_unallocated_people(self):
        """Tests that the unallocated people are printed on the screen"""
        self.amity.add_person('FELLOW', 'Wanjiru', 'N')
        self.amity.print_unallocated()
        message = sys.stdout.getvalue().strip()
        self.assertIn("Wanjiru", message)

    def test_print_unallocated_people_to_txt_file(self):
        """Tests that the unallocated people are printed on a txt file"""
        self.amity.add_person('FELLOW', 'Cynthia', 'N')
        self.amity.print_unallocated('test_unallocated')
        message = sys.stdout.getvalue().strip()
        self.assertIn("Printing to test_unallocated completed", message)

    def test_print_office_allocations_to_a_txt_file(self):
        """Tests that the allocated people are printed on a txt file"""
        self.amity.create_room('OFFICE', 'test_office')
        self.amity.add_person('FELLOW', 'Steve', 'N')
        self.amity.print_allocations('test_allocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn("Printing to test_allocations complete", message)

    def test_load_people(self):
        """Tests that people can be loaded to the system using a txt file"""
        initial_count = len(self.amity.all_people['fellow'] +
                            self.amity.all_people['staff'])
        self.amity.load_people('tests')
        final_count = len(self.amity.all_people['fellow'] +
                          self.amity.all_people['staff'])
        self.assertGreater(final_count, initial_count)

    def test_load_people_from_not_existent_txt_file(self):
        """ Tests that peole cannot be loaded from a non existent file"""
        self.amity.load_people('test')
        message = sys.stdout.getvalue().strip()
        self.assertIn("That file does not exist...", message)

    def test_print_all_rooms_on_screen(self):
        """ Tests that all rooms can be printed on the screen """
        self.amity.create_room('OFFICE', 'test_office')
        self.amity.print_all_rooms()
        message = sys.stdout.getvalue().strip()
        self.assertIn("test_office", message)

    def test_print_all_rooms_on_txt(self):
        """ Tests that all rooms can be printed on a txt file """
        self.amity.create_room('OFFICE', 'test_office')
        self.amity.print_all_rooms('test')
        message = sys.stdout.getvalue().strip()
        self.assertIn("***Done***", message)

    def test_print_all_people(self):
        """ Tests that all people can be printed on the screen """
        self.amity.add_person('FELLOW', 'print_all')
        self.amity.print_all_people()
        message = sys.stdout.getvalue().strip()
        self.assertIn("print_all", message)



if __name__ == '__main__':
    unittest.main()
