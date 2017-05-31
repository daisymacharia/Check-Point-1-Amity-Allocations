import random

from amity.Model.person import Fellow, Staff
from amity.Model.room import LivingSpace, Office
from termcolor import cprint
import pickle
import sqlite3
from os import remove
from sqlite3 import Error
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class Amity():
    """Holds the main functions to be called by other classes"""

    all_rooms = {'office': [], 'livingspace': []}
    all_people = {'staff': [], 'fellow': []}
    waiting_list = {'office': [], 'livingspace': []}

    def create_room(self, room_type, room_name):
        """Creates new offices and living spaces and stores them in lists"""
        # check if room already exists
        for room in self.all_rooms['office'] + self.all_rooms['livingspace']:
            if room.room_name == room_name:
                cprint("{} already exists".format(room_name), "red")
                return
        # create office space
        if room_type == "OFFICE":
            new_office = Office(room_name)
            self.all_rooms['office'].append(new_office)
            cprint("Office {} created successfully".format(
                   new_office.room_name), "cyan")
        # create living space
        elif room_type == "LIVINGSPACE":
            new_livingspace = LivingSpace(room_name)
            self.all_rooms['livingspace'].append(new_livingspace)
            cprint("Livingspace {} created successfully".format(
                   new_livingspace.room_name), "cyan")

        elif room_type not in ["LIVINGSPACE" ''"OFFICE"]:
            cprint("Invalid room type", "red")

    def allocate_room(self, room_type, person_object):
        """generates a random room from a list of available rooms whenever it
           is called and allocates a room to person
         """
        if room_type == "OFFICE":
            available_offices = [room for room in self.all_rooms['office']
                                 if len(room.room_occupants) < room.capacity]
            if available_offices:
                allocated_office = random.choice(available_offices)
                allocated_office.room_occupants.append(person_object)
                cprint("{} added to office {}".format(
                       person_object.person_name,
                       allocated_office.room_name), "cyan")
            else:
                self.waiting_list['office'].append(person_object)
                cprint("No available rooms, you'll be added to the office"
                       + " " + "waiting list", "red")
        elif room_type == "LIVINGSPACE":
            available_livingspaces = [room for room in self.all_rooms[
                                      'livingspace']
                                      if len(room.room_occupants) <
                                      room.capacity]
            if available_livingspaces:
                allocated_livingspace = random.choice(available_livingspaces)
                allocated_livingspace.room_occupants.append(person_object)
                cprint("{} successfully added to living space {}".
                       format(person_object.person_name,
                              allocated_livingspace.room_name), "cyan")
            else:
                self.waiting_list['livingspace'].append(person_object)
                cprint("No available rooms, you'll be added to the"
                       + " " + "livingspace waiting list", "red")
        elif room_type not in ["LIVINGSPACE" ''"OFFICE"]:
            cprint("Invalid room type", "red")

    def add_person(self, person_type, person_name, want_accomodation=""):
        """ adds a new person whether staff or fellow """
        # check if the name contains digits
        is_digit = any(char.isdigit() for char in person_name)
        if is_digit:
            cprint("Invalid name. Use letters only", 'red')
            return
        # check if person exists in the system
        for person in self.all_people['staff'] + self.all_people['fellow']:
            if person.person_name == person_name:
                cprint("{} already exists".format(person_name), "red")
                return
        # add a new staff member
        if person_type == "STAFF":
            staff_object = Staff(person_name)
            staff_object.person_id = "S" + "-" + str(staff_object.person_id)
            self.all_people['staff'].append(staff_object)
            cprint("Staff {} ID: {} added successfully".format(
                   staff_object.person_name,  staff_object.person_id), "cyan")
            self.allocate_room("OFFICE", staff_object)
            if want_accomodation == "Y":
                cprint("Staff cannot be allocated a living space", "red")
        # add a new fellow member
        elif person_type == "FELLOW":
            fellow_object = Fellow(person_name)
            fellow_object.person_id = "F" + "-" + str(fellow_object.person_id)
            self.all_people['fellow'].append(fellow_object)
            cprint("Fellow {} ID: {} added successfully".format(
                   fellow_object.person_name, fellow_object.person_id), "cyan")
            self.allocate_room("OFFICE", fellow_object)
            if want_accomodation == "Y":
                self.allocate_room("LIVINGSPACE", fellow_object)
        elif person_type not in ["STAFF", "FELLOW"]:
            cprint("Invalid person type", "red")

    def remove_person_from_previous_office(self, p_id):

        """ Removes a staff or fellow from the offices they were previously
            located in or from the waiting list if they did not have
            a livingspace """
        for room in self.all_rooms['office']:
            for person in room.room_occupants:
                if person.person_id == p_id:
                    room.room_occupants.remove(person)
                    cprint("{} removed from previous office".format
                           (person.person_name), "cyan")
                    return
        for person in self.waiting_list['office']:
            if person.person_id == p_id:
                self.waiting_list['office'].remove(person)
                cprint("{} removed from waiting list".format(
                       person.person_name), "cyan")

    def remove_person_from_previous_livingspace(self, p_id):
        """ Removes a fellow from the living spaces they were previously
            located in or from the waiting list if they did not have a
            livingspace """
        for room in self.all_rooms['livingspace']:
            for person in room.room_occupants:
                if person.person_id == p_id:
                    room.room_occupants.remove(person)
                    cprint("{} removed from previous livingspace"
                           .format(person.person_name), "cyan")
                    return
        for person in self.waiting_list['livingspace']:
            if person.person_id == p_id:
                self.waiting_list['livingspace'].remove(person)
                cprint("{} removed from waiting list".format(
                       person.person_name), "cyan")

    def reallocate_staff(self, p_id, new_room_name):
        """ Reallocate a staff to a different office and rejects allocation to
            a living space """
        room = [room for room in self.all_rooms['office'] +  self.all_rooms[
                'livingspace'] if room.room_name == new_room_name]
        person = [person for person in self.all_people['staff']
                  if person.person_id == p_id]
        if room:
            if room[0].room_type == "office":
                for person_obj in room[0].room_occupants:
                    # checks if person already exists in the new office
                    if person_obj.person_id == p_id:
                        cprint("{} already exists in the room {}".format(
                               person[0].person_name, new_room_name), "red")
                        return
                # reallocate a person and call function
                # remove_person_from_previous_office
                # to remove the staff from the previous
                # office or waiting list
                if len(room[0].room_occupants) < 6:
                    self.remove_person_from_previous_office(p_id)
                    room[0].room_occupants.append(person[0])
                    cprint("{} has been reallocated to office {} ".format(
                           person[0].person_name, new_room_name), "cyan")
                    return
                else:
                    cprint("Office {} is full, choose another room".format(
                           new_room_name), "red")
                    return

            elif room[0].room_type == "livingspace":
                cprint("Cannot reallocate a staff to a living space",
                       "red")
                return
        else:
            cprint("{} does not exist".format(new_room_name), "red")

    def reallocate_fellow(self, p_id, new_room_name):
        """ Reallocate a fellow to a different office or living space """
        room = [room for room in self.all_rooms['office'] +  self.all_rooms[
                'livingspace'] if room.room_name == new_room_name]
        person = [person for person in self.all_people['fellow']
                  if person.person_id == p_id]

        if room:
            if room[0].room_type == "office":
                for person_obj in room[0].room_occupants:
                    # checks if person already exists in the new office
                    if person_obj.person_id == p_id:
                        cprint("{} already exists in the room {}".format(
                               person[0].person_name, new_room_name), "red")
                        return
                if len(room[0].room_occupants) < 6:
                    self.remove_person_from_previous_office(p_id)
                    room[0].room_occupants.append(person[0])
                    cprint("{} has been reallocated to office {} ".format(
                           person[0].person_name, new_room_name), "cyan")
                    return
                else:
                    cprint("Office {} is full, choose another room".format(
                           new_room_name), "red")
                    return
            elif room[0].room_type == "livingspace":
                for person_obj in room[0].room_occupants:
                    if person_obj.person_id == p_id:
                        cprint("{} already exists in the room {}".format(
                               person[0].person_name, new_room_name), "red")
                        return
                if len(room[0].room_occupants) < 4:
                    self.remove_person_from_previous_livingspace(p_id)
                    room[0].room_occupants.append(person[0])
                    cprint("{} has been reallocated to livingspace {}"
                           .format(person[0].person_name, new_room_name
                           ), "cyan")
                    return
                else:
                    cprint("Livingspace {} is full, choose another room"
                           .format(new_room_name), "red")
                    return
        else:
            cprint("{} does not exist".format(new_room_name), "red")

    def reallocate_person(self, p_id, new_room_name):
        """ Reallocate a person to a different office or living space """
        people =  self.all_people['staff'] + self.all_people['fellow']
        person = [person for person in people if person.person_id == p_id]
        if person:
            if person[0].person_type == "staff":
                self.reallocate_staff(p_id, new_room_name)
            elif person[0].person_type == "fellow":
                self.reallocate_fellow(p_id, new_room_name)
        else:
            cprint("{} does not exist".format(p_id), "red")

    def load_people(self, filename):
        """ Collects details about employees from a .txt file and
            adds them to the system """
        try:
            if filename:
                filepath = 'amity/files/' + filename + '.txt'
                load_people_file = open(filepath)
                for line in load_people_file.read().splitlines():
                    if len(line) == 0:
                        continue
                    list_words = line.split(' ')
                    first_name = list_words[0]
                    last_name = list_words[1]
                    person_name = first_name+' '+last_name
                    person_type = list_words[2]
                    try:
                        want_accomodation = list_words[3]
                        self.add_person(person_type, person_name,
                                        want_accomodation)
                    except IndexError:
                        want_accomodation = 'N'
                        cprint('*'*60 + '\n', 'white')
                        self.add_person(person_type, person_name,
                                        want_accomodation)
                        cprint('*'*60 + '\n', 'white')
        except Exception:
            cprint('That file does not exist...', "red")

    def print_unallocated(self, filename=None):
        """ Prints a list of the people still waiting to be
            allocated into rooms """
        try:
            if filename:
                filepath = 'amity/files/' + filename + '.txt'
                print_unallocated_file = open(filepath, 'w')
                print_unallocated_file.write("UNALLOCATED TO OFFICES...\n")
                print_unallocated_file.write('*'*60 + '\n')
                for person in self.waiting_list['office']:
                    print_unallocated_file.write('\t' + person.person_name + ',')
                print_unallocated_file.write('\n\n')
                print_unallocated_file.write("UNALLOCATED TO LIVINGSPACES...\n")
                print_unallocated_file.write('*'*60 + '\n')
                for person in self.waiting_list['livingspace']:
                    print_unallocated_file.write('\t' + person.person_name + ',')
                print_unallocated_file.close()
                cprint('Printing to {} completed'.format(
                       filename), "white")
            else:
                cprint("\n UNALLOCATED TO OFFICES...\n", 'cyan')
                cprint('*'*60 + '\n')
                for person in self.waiting_list['office']:
                    cprint(person.person_name, "yellow")
                cprint("UNALLOCATED TO OFFICES...\n", 'cyan')
                cprint('*'*60 + '\n')
                for person in self.waiting_list['livingspace']:
                    cprint(person.person_name, "yellow")
        except ValueError:
            cprint("An error occured while printing. Please try again", "red")

    def print_room(self, roomname):
        """ print the room occupants in a specified room """
        room = [room for room in self.all_rooms['office'] + self.all_rooms[
                'livingspace'] if room.room_name == roomname]
        members = [people for people in room[0].room_occupants]
        if room:
            if members:
                cprint('{} NAME: {} \n'.format(room[0].room_type.upper(),
                       room[0].room_name), "white")
                cprint('*'*60, "cyan")
                for person in members:
                    cprint('\t' + person.person_name + ',', "magenta")
                print('\n')
            else:
                cprint("There are no occupants in room {}"
                           .format(room[0].room_name), "red")
                return
        else:
            cprint("Room {} does not exist".format(roomname), "red")

    def print_office_allocations(self):
        # checks if that the list has offices
            if self.all_rooms['office']:
                cprint('OFFICES...\n', "white")
                for room in self.all_rooms['office']:
                    self.print_room(room.room_name)
            else:
                cprint("No offices created at the moment")

    def print_livingspace_allocations(self):
        # checks if that the list has livingspaces
            if self.all_rooms['livingspace']:
                cprint('LIVING SPACES...\n', "white")
                for room in self.all_rooms['livingspace']:
                    self.print_room(room.room_name)
            else:
                cprint("No livingspaces created at the moment")

    def print_allocations(self, filename=None):
        try:
            if filename:
                filepath = 'amity/files/' + filename + '.txt'
                print_allocations_file = open(filepath, 'w')
                print_allocations_file.write("OFFICES...\n")
                for room in self.all_rooms['office']:
                    print_allocations_file.write('\n\t' + room.room_name +
                                                 '\n' + '-' * 90 + '\n')
                    if room.room_occupants:
                        for person in room.room_occupants:
                            print_allocations_file.write('\t' + person.person_name + ',')
                    else:
                        print_allocations_file.write("No occupants")
                    print_allocations_file.write('\n\n')
                print_allocations_file.write("LIVINGSPACES...\n")
                for room in self.all_rooms['livingspace']:
                    print_allocations_file.write('\n\t' + room.room_name +
                                                 '\n' + '-' * 90 + '\n')
                    if room.room_occupants:
                        for person in room.room_occupants:
                            print_allocations_file.write('\t' + person.person_name + ',')
                    else:
                        print_allocations_file.write("No occupants")
                    print_allocations_file.write('\n')
                print_allocations_file.close()
                cprint('Printing to {} complete'.format(
                       filename), "cyan")
                return
            else:
                self.print_office_allocations()
                self.print_livingspace_allocations()
                return
        except Exception:
            cprint("An error occured while printing. Please try again", "red")

    def delete_person(self, p_id):
        """ Delete the records of a specific person from the system"""
        rooms = [room for room in self.all_rooms['office'] +
                self.all_rooms['livingspace']]
        person = [person for person in self.all_people['fellow'] +
                  self.all_people['staff'] if  person.person_id == p_id]
        if person:
            if person[0].person_type == 'fellow':
                self.all_people['fellow'].remove(person[0])
                cprint('Fellow {} deleted'.format(person[0].person_name), 'cyan')
            elif person[0].person_type == 'staff':
                self.all_people['staff'].remove(person[0])
                cprint('Staff {} deleted'.format(person[0].person_name), 'cyan')
            for room in rooms:
                if person[0] in room.room_occupants:
                    room.room_occupants.remove(person[0])
        else:
            cprint("{} does not exist".format(p_id), 'red')

    def delete_room(self, roomname):
        """ Delete the records of a specific room from the system"""
        rooms = [room for room in self.all_rooms['office'] +
                self.all_rooms['livingspace'] if room.room_name == roomname]
        if rooms:
            if rooms[0].room_type == 'office':
                for person in rooms[0].room_occupants:
                    self.waiting_list['office'].append(person)
                self.all_rooms['office'].remove(rooms[0])
                cprint('Office {} deleted'.format(roomname), 'cyan')
            elif rooms[0].room_type == 'livingspace':
                for person in rooms[0].room_occupants:
                    self.waiting_list['livingspace'].append(person)
                self.all_rooms['livingspace'].remove(rooms[0])
                cprint('Living space {} deleted'.format(roomname), 'cyan')
        else:
            cprint("{} does not exist" .format(roomname), 'red')


    def save_state(self, db_file):

        """ Persists all the data stored in the app to an SQLite database
        set the directory path
        connect to the database
        create a table if none exists and push the data to it
        save all the data into the database
        close the database connection
        """

        path = 'amity/Database/'
        db_connect = sqlite3.connect(path + db_file)
        conn = db_connect.cursor()

        conn.execute("CREATE TABLE IF NOT EXISTS all_data "
                     "(dataID INTEGER PRIMARY KEY UNIQUE, "
                     "all_rooms TEXT, all_people TEXT, waiting_list TEXT)")

        all_rooms = pickle.dumps(Amity.all_rooms)
        all_people = pickle.dumps(Amity.all_people)
        waiting_list = pickle.dumps(Amity.waiting_list)

        conn.execute("INSERT INTO all_data VALUES (null, ?, ?, ?);",
                     (all_rooms, all_people, waiting_list))

        db_connect.commit()
        db_connect.close()

        cprint('Data successfully exported to Database', 'cyan')

    def load_state(self, db_file):

        """ Loads data from a database into the application
        set the directory path
        connect to the database
        select all data from the database table
        load the data into the application
        close the database connection

        """
        try:
            path = 'amity/Database/'
            db_connect = sqlite3.connect(path + db_file)
            conn = db_connect.cursor()

            conn.execute("SELECT * FROM all_data WHERE dataID = (SELECT MAX(dataID) FROM all_data)")
            data = conn.fetchone()

            Amity.all_rooms = pickle.loads(data[1])
            Amity.all_people = pickle.loads(data[2])
            Amity.waiting_list = pickle.loads(data[3])

            db_connect.close()
            cprint('Successfully loaded data from the Database.', "cyan")

        except Error:
            remove(path + db_file)
            cprint ("Database not found, Please check the name and try again!",
                    red)
