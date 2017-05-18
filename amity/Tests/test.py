import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from io import StringIO
from Model.person import Staff, Fellow
from Model.room import Office, LivingSpace
from amity import Amity


class TestPeople(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()
        self.amity.all_persons = {'staff': [Staff('test_staff')],
                                  'fellow': [Fellow('test_fellow')]
                                  }
        self.amity.all_rooms = {'livingspace': [LivingSpace('test_livingspace')],
                                'office': [Office('test_office')]}

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
        initial_staff_count = len(self.amity.all_people['staff'])
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
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_fellow already exists', message)

    def test_fellow_is_allocated_a_living_space(self):
        """Tests that a fellow member is allocated a living space"""
        self.amity.add_person('FELLOW', 'Ivy', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Ivy successfully added to living space test_livingspace',
                      message)

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
        initial_livingspace_count = len(self.amity.all_rooms['livingspace'])
        self.amity.create_room('LIVINGSPACE', 'newlivingspace')
        new_livingspace_count = len(self.amity.all_rooms['livingspace'])
        self.assertGreater(new_livingspace_count, initial_livingspace_count)

    def test_cannot_create_livingspace_with_same_name(self):
        """Tests that a existing livingspace cannot be created"""
        self.amity.create_room('LIVINGSPACE', 'test_livingspace')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_livingspace already exists', message)

    def test_cannot_create_livingspace_with_wrong_room_type(self):
        """Tests that a new livingspace is not created when wrong room type is
           inputted"""
        self.amity.create_room('Wrong_input', 'test_wrong_livingspace')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Invalid room type', message)

    def test_reallocation_of_fellow_to_new_office(self):
        """Tests that a fellow is successfully reallocated to a new office"""
        self.amity.create_room('OFFICE', 'test_office_reallocations')
        self.amity.reallocate_fellow('test_fellow', 'test_office_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_fellow has been reallocated successfully to office test_office_reallocations', message)

    def test_reallocation_of_fellow_to_new_living_space(self):
        """Tests that a fellow is successfully reallocated to a new
           living space"""
        self.amity.create_room('LIVINGSPACE', 'test_livingspace_reallocations')
        self.amity.reallocate_fellow('Ivy', 'test_livingspace_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Ivy has been reallocated successfully to livingspace test_livingspace_reallocations', message)

    def test_reallocation_of_staff_to_new_office(self):
        """Tests that a staff is successfully reallocated to a new office"""
        self.amity.create_room('OFFICE', 'test_office_reallocations_for_staff')
        self.amity.reallocate_staff('test_staff',
                                    'test_office_reallocations_for_staff')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_staff has been reallocated successfully to office test_office_reallocations_for_staff', message)

    def test_reallocated_fellow_is_removed_from_previous_office(self):
        """Tests that a fellow is removed from the previous room once they are
           reallocated to a new office"""
        # add fellow test_fellow_reallocations who is allocated an office
        self.amity.create_room('OFFICE', 'test_office_reallocations')
        self.amity.reallocate_fellow('test_fellow', 'test_office_reallocations')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_fellow sucessfully removed from previous office', message)

    def test_reallocated_fellow_is_removed_from_previous_livingspace(self):
        """Tests that a fellow is removed from the previous livingspace once
           they are reallocated to a new livingspace """
        self.amity.add_person('FELLOW', 'test_fellow_reallocation', "Y")
        self.amity.create_room('LIVINGSPACE', 'test_livingspace_removal_of_fellow')
        self.amity.reallocate_fellow('test_fellow_reallocation',
                                     'test_livingspace_removal_of_fellow')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_fellow_reallocation sucessfully removed from previous livingspace', message)

    def test_reallocated_staff_is_removed_from_previous_office(self):
        """Tests that a staff is removed from the previous office once they are
           reallocated to a new office"""
        # add staff test_staff_allocations who is allocated an office
        self.amity.add_person('STAFF', 'test_staff_reallocation')
        self.amity.create_room('OFFICE', 'test_office_removal_of_staff')
        self.amity.reallocate_staff('test_staff_reallocation',
                                    'test_office_removal_of_staff')
        message = sys.stdout.getvalue().strip()
        self.assertIn('test_staff_reallocation sucessfully removed from previous office', message)

    def test_cannot_reallocated_staff_to_a_livingspace(self):
        """Tests that a staff is not reallocated to a living space"""
        self.amity.create_room('LIVINGSPACE', 'test_reallocations_staff')
        self.amity.reallocate_staff('test_staff',
                                    'test_reallocations_staff')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Cannot reallocate a staff member to a living space', message)

    def test_removes_people_from_waiting_list_after_allocation(self):
        self.amity.create_room('OFFICE', 'Red')
        self.amity.load_people("people")
        self.reallocate_person('DAISY MACHARIA', 'Red')
        message = sys.stdout.getvalue().strip()
        self.assertIn('DAISY MACHARIA sucessfully removed from waiting list')

    def test_fellow_cannot_be_reallocated_to_a_full_office(self):
        pass

    def test_fellow_cannot_be_reallocated_to_a_full_livingspace(self):
        pass

    def test_staff_cannot_be_reallocated_to_a_full_office(self):
        pass

    def test_print_room(self):
        pass

    def test_print_unallocated_people(self):
        pass

    def test_print_unallocated_people_to_txt_file(self):
        pass

    def test_print_office_allocations_to_a_txt_file(self):
        pass

    def test_load_people(self):
        pass

    def test_load_people_from_not_existent_txt_file(self):
        pass

    def test_save_state(self):
        pass

    def test_load_state(self):
        pass





if __name__ == '__main__':
    unittest.main()
