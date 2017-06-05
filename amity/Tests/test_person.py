from io import StringIO
from amity.Controller.amity import Amity
from amity.Model.person import Fellow, Staff
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestPeople(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.tearDown()

    def tearDown(self):

        self.held, sys.stdout = sys.stdout, StringIO()
        self.amity.all_people = {'staff': [], 'fellow': []}
        self.amity.all_rooms = {'livingspace': [], 'office': []}

    def test_person_name_is_not_digit(self):
        """Tests that the person name can only be a string"""
        self.amity.add_person('STAFF', '456', 'N')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Invalid name. Use letters only', message)

    def test_add_staff_member(self):
        """Tests that the length of the list_of_staff increases after
        adding a new staff member"""
        initial_people_count = len(self.amity.all_people['staff'])
        self.amity.add_person('STAFF', 'Daisy', 'N')
        new_people_count = len(self.amity.all_people['staff'])
        self.assertGreater(new_people_count, initial_people_count)

    def test_cannot_create_staff_with_same_name(self):
        """Tests that the length of the list_of_staff does not increases
        after adding a staff member that already exists"""
        self.amity.add_person('STAFF', 'test_staff', 'N')
        self.amity.add_person('STAFF', 'test_staff', 'N')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_staff already exists', message)

    def test_staff_cannot_be_allocated_a_living_space(self):
        """Tests that a staff member cannot be allocated a living space"""
        self.amity.add_person('STAFF', 'Muthoni', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Staff cannot be allocated a living space', message)

    def test_add_fellow(self):
        """Tests that the length of the list_of_fellows increases after
        adding a new fellow member"""
        initial_fellow_count = len(self.amity.all_people['fellow'])
        self.amity.add_person('FELLOW', 'Wanjiru', 'N')
        new_fellow_count = len(self.amity.all_people['fellow'])
        self.assertGreater(new_fellow_count, initial_fellow_count)

    def test_cannot_create_fellows_with_same_name(self):
        """Tests that the length of the list_of_fellows does not increase
        after adding a fellow member that already exists"""
        self.amity.add_person('FELLOW', 'test_fellow', 'N')
        self.amity.add_person('FELLOW', 'test_fellow', 'N')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_fellow already exists', message)

    def test_fellow_is_allocated_a_living_space(self):
        """Tests that a fellow member is allocated a living space"""
        self.amity.create_room('LIVINGSPACE', 'test_livingspace')
        self.amity.add_person('FELLOW', 'Ivy', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Ivy successfully added to living space'
                      , message)

    def test_reallocation_of_fellow_to_new_office(self):
        """Tests that a fellow is successfully reallocated to a new office"""
        self.amity.create_room('OFFICE', 'test_reallocations')
        fellow_obj = Fellow("test_fellow")
        self.amity.all_people['fellow'].append(fellow_obj)
        self.amity.reallocate_person(fellow_obj.person_id,'test_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_fellow has been reallocated to office'
                      + " " + 'test_reallocations', message)

    def test_reallocation_of_fellow_to_new_living_space(self):
        """Tests that a fellow is successfully reallocated to a new
           living space"""
        self.amity.create_room('LIVINGSPACE', 'test_living_reallocations')
        fellow_obj = Fellow("Tumbo")
        self.amity.all_people['fellow'].append(fellow_obj)
        self.amity.reallocate_person(fellow_obj.person_id,'test_living_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Tumbo has been reallocated to livingspace'
                      + " " + 'test_living_reallocations', message)

    def test_reallocation_of_staff_to_new_office(self):
        """Tests that a staff is successfully reallocated to a new office"""
        self.amity.create_room('OFFICE', 'test_office_reallocations')
        staff_obj = Staff("Macharia")
        self.amity.all_people['staff'].append(staff_obj)
        self.amity.reallocate_person(staff_obj.person_id,'test_office_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Macharia has been reallocated to office'
                      + " " + 'test_office_reallocations', message)

    def test_cannot_reallocated_staff_to_a_livingspace(self):
        """Tests that a staff is not reallocated to a living space"""
        self.amity.create_room('LIVINGSPACE', 'test_staff_reallocations')
        staff_obj = Staff("Cynthia")
        self.amity.all_people['staff'].append(staff_obj)
        self.amity.reallocate_person(staff_obj.person_id,'test_staff_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Cannot reallocate a staff to a living space', message)

    def test_removes_people_from_waiting_list_after_reallocation(self):
        """Tests that reallocations of people on waiting lists removes them from
         the waiting list"""
        self.amity.add_person('FELLOW', 'Ivy')
        self.amity.create_room('OFFICE', 'Red')
        self.amity.reallocate_person(self.amity.all_people['fellow'][0].person_id,'Red')
        message = sys.stdout.getvalue().strip()
        self.assertIn(self.amity.all_people['fellow'][0].person_name + " "
                      'removed from waiting list', message)

    def test_removes_people_from_previous_office(self):
        """Tests that reallocations of people to office removes them
           from previous office """
        self.amity.create_room('OFFICE', 'Blue')
        self.amity.add_person('FELLOW', 'Ivy')
        self.amity.create_room('OFFICE', 'Red')
        self.amity.reallocate_person(self.amity.all_people['fellow'][0].person_id,'Red')
        message = sys.stdout.getvalue().strip()
        self.assertIn(self.amity.all_people['fellow'][0].person_name + " "
                      'removed from previous office', message)

    def test_removes_people_from_previous_livingspace(self):
        """Tests that reallocations of people to living spaces removes them
           from previous living spaces"""
        self.amity.create_room('LIVINGSPACE', 'Blue')
        self.amity.add_person('FELLOW', 'Ivy', 'Y')
        self.amity.create_room('LIVINGSPACE', 'Red')
        self.amity.reallocate_person(self.amity.all_people['fellow'][0].person_id,'Red')
        message = sys.stdout.getvalue().strip()
        self.assertIn(self.amity.all_people['fellow'][0].person_name + " "
                      'removed from previous livingspace', message)

    def test_delete_person(self):
        """ Tests that a user is deleted from the system and from the rooms
            they currently are allocated """
        person_obj = Staff("Njoki")
        self.amity.all_people['staff'].append(person_obj)
        self.amity.create_room('OFFICE', 'Blue')
        self.amity.reallocate_person(person_obj.person_id,'Blue')
        self.amity.delete_person(person_obj.person_id)

        for person in self.amity.all_people['staff']:
            self.assertNotIn("Njoki", person.person_name)
        for room in self.amity.all_rooms['office']:
            for person in room.room_occupants:
                self.assertNotIn(person_obj, room.room_occupants)

if __name__ == '__main__':
    unittest.main()
