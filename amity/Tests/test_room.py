import unittest
import os
from room.room import Office, LivingSpace
from amity import Amity
from io import StringIO

'''
  assert
  assertIn(A, B)
  assertNotIn(a, b)
  assertGreater(a, b)
  assertLess(a, b)
  assertTrue (2+2, 4)
  assertFalse(2-2, 1)
  assertEquals(1, 1)
  assertNotEqual(1+4, 8)
'''

class TestRoom(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_create_office(self):
        """Tests that a new office is created successfully"""
        initial_office_count = len(self.dojo.list_of_offices)
        #initial length of office list before creating a new office
        self.amity.create_room('OFFICE', 'newoffice')
        new_office_count = len(self.amity.list_of_offices)
        #new length of office list after creation of office
        self.assertGreater(new_office_count, initial_office_count)

    def test_cannot_create_office_with_same_name(self):
        """Tests that a existing office cannot be created"""
        initial_office_count = len(self.amity.list_of_offices)
        self.amity.create_room('OFFICE', 'test_office')
        new_office_count = len(self.amity.list_of_offices)
        self.assertEquals(new_office_count, initial_office_count)

    def test_cannot_create_office_with_wrong_room_type(self):
        """Tests that a new office is not created when wrong room type is inputted"""
        self.amity.create_room('Wrong_input', 'test_office')
        message = sys.stdout.getvalue().strip()
        self.assertEquals(str(message), "Invalid room type")

    def test_create_livingspace(self):
        """Tests that a new livingspace is created successfully"""
        initial_livingspace_count = len(self.amity.list_of_livingspaces)
        self.amity.create_room('LIVINGSPACE', 'newlivingspace')
        new_livingspace_count = len(self.amity.list_of_livingspaces)
        self.assertGreater(new_livingspace_count, initial_livingspace_countt)

    def test_cannot_create_livingspace_with_same_name(self):
        """Tests that a existing livingspace cannot be created"""
        initial_livingspace_count = len(self.amity.list_of_livingspaces)
        self.amity.create_room('LIVINGSPACE', 'test_livingspace')
        new_livingspace_count = len(self.amity.list_of_livingspaces)
        self.assertEquals(new_livingspace_count, initial_livingspace_count)

    def test_cannot_create_livingspace_with_wrong_room_type(self):
        """Tests that a new livingspace is not created when wrong room type is inputted"""
        self.amity.create_room('Wrong_input', 'test_livingspace')
        message = sys.stdout.getvalue().strip()
        self.assertEquals(str(message), "Invalid room type")

    
