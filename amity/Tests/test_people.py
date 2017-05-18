import unittest
import os
from io import StringIO
from person.person import Staff
from amity import Amity


class TestPeople(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_add_staff_member(self):
        """Tests that the length of the list_of_staff increases after
        adding a new staff member"""
        initial_people_count = len(self.amity.list_of_staff)
        self.amity.add_person('STAFF', 'Daisy', 'N')
        new_people_count = len(self.amity.list_of_staff)
        self.assertGreater(new_people_count, initial_people_count)

    def test_cannot_create_staff_with_same_name(self):
        """Tests that the length of the list_of_staff does not increases
        after adding a staff member that already exists"""
        initial_staff_count = len(self.amity.list_of_staff)
        self.amity.add_person('STAFF', 'test_staff', 'N')
        new_staff_count = len(self.amity.list_of_staff)
        self.assertEquals(new_staff_count, initial_staff_count)

    def test_staff_cannot_be_allocated_a_living_space(self):
        """This tests that a staff member cannot be allocated a living space"""
        self.amity.add_person('STAFF', 'test_staff', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Staff cannot be allocated a living space', message)

    def test_add_fellow(self):
        """Tests that the length of the list_of_fellows increases after
        adding a new fellow member"""
        initial_fellow_count = len(self.amity.list_of_fellows)
        self.amity.add_person('FELLOW', 'Wanjiru', 'N')
        new_fellow_count = len(self.amity.list_of_fellows)
        self.assertGreater(new_fellow_count, initial_fellow_count)

    def test_cannot_create_fellows_with_same_name(self):
        """Tests that the length of the list_of_fellows does not increase
        after adding a fellow member that already exists"""
        initial_fellow_count = len(self.amity.list_of_fellows)
        self.amity.add_person('FELLOW', 'test_fellow', 'N')
        new_fellow_count = len(self.amity.list_of_fellows)
        self.assertEquals(new_fellow_count, initial_fellow_count)

    def test_fellow_is_allocated_a_living_space(self):
        """This tests that a fellow member is allocated a living space"""
        self.amity.add_person('FELLOW', 'test_', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Staff cannot be allocated a living space', message)
