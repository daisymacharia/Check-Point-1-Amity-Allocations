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
        self.amity.all_people = {'staff': [], 'fellow': []}

        def test_create_office(self):
            """Tests that a new office is created successfully"""
            initial_office_count = len(self.amity.all_rooms['office'])
            # initial length of office list before creating a new office
            self.amity.create_room('OFFICE', 'newoffice')
            new_office_count = len(self.amity.all_rooms['office'])
            # new length of office list after creation of office
            self.assertGreater(new_office_count, initial_office_count)

        def test_cannot_create_office_with_same_name(self):
            """Tests that a existing office cannot be created"""
            self.amity.create_room('OFFICE', 'test_office')
            self.amity.create_room('OFFICE', 'test_office')
            message = sys.stdout.getvalue().strip()
            self.assertIn('test_office already exists', message)

        def test_cannot_create_office_with_wrong_room_type(self):
            """Tests that a new office is not created when wrong room type is
               inputted"""
            self.amity.create_room('Wrong_input', 'test_wrong_office')
            message = sys.stdout.getvalue().strip()
            self.assertIn('Invalid room type', message)

        def test_create_livingspace(self):
            """Tests that a new living space is created successfully"""
            initial_living_count = len(self.amity.all_rooms['livingspace'])
            self.amity.create_room('LIVINGSPACE', 'newlivingspace')
            new_living_count = len(self.amity.all_rooms['livingspace'])
            self.assertGreater(new_living_count, initial_living_count)

        def test_cannot_create_livingspace_with_same_name(self):
            """Tests that a existing livingspace cannot be created"""
            self.amity.create_room('LIVINGSPACE', 'test_livingspace')
            self.amity.create_room('LIVINGSPACE', 'test_livingspace')
            message = sys.stdout.getvalue().strip()
            self.assertIn('test_livingspace already exists', message)

        def test_cannot_create_livingspace_with_wrong_room_type(self):
            """Tests that a new livingspace is not created when wrong room type is
               inputted"""
            self.amity.create_room('Wrong_input', 'test_wrong_livingspace')
            message = sys.stdout.getvalue().strip()
            self.assertIn('Invalid room type', message)

        def test_delete_room(self):
            """Tests that a room can be deleted and the occupants in the room
               moved to the waiting list """
            self.amity.create_room('OFFICE', 'test_delete')
            self.amity.delete_room('test_delete')


if __name__ == '__main__':
    unittest.main()
