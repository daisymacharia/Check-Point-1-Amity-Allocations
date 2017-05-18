import random

from Model.person import Fellow, Staff
from Model.room import LivingSpace, Office
from termcolor import cprint


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
                allocated_office.room_occupants.append(
                                                     person_object.person_name)
                cprint("{} added to office {}".format(
                       person_object.person_name,
                       allocated_office.room_name), "cyan")
            else:
                self.waiting_list['office'].append(person_object.person_name)
                cprint("No available rooms, you'll be added to the office waiting list", "red")
        elif room_type == "LIVINGSPACE":
            available_livingspaces = [room for room in self.all_rooms[
                                      'livingspace']
                                      if len(room.room_occupants) <
                                      room.capacity]
            if available_livingspaces:
                allocated_livingspace = random.choice(available_livingspaces)
                allocated_livingspace.room_occupants.append(
                                                     person_object.person_name)
                cprint("{} successfully added to living space {}".format(person_object.person_name,
                       allocated_livingspace.room_name), "cyan")
            else:
                self.waiting_list['livingspace'].append(
                                                    person_object.person_name)
                cprint("No available rooms, you'll be added to the livingspace waiting list", "red")
        elif room_type not in ["LIVINGSPACE" ''"OFFICE"]:
            cprint("Invalid room type", "red")

    def add_person(self, person_type, person_name, want_accomodation="N"):
        """ adds a new person whether staff or fellow """
        # check if person exists in the system
        for person in self.all_people['staff'] + self.all_people['fellow']:
            if person.person_name == person_name:
                cprint("{} already exists".format(person_name), "red")
                return
        # add a new staff member
        if person_type == "STAFF":
            staff_object = Staff(person_name)
            self.all_people['staff'].append(staff_object)
            cprint("Staff {} added successfully".format(
                   staff_object.person_name), "cyan")
            self.allocate_room("OFFICE", staff_object)
            if want_accomodation == "Y":
                cprint("Staff cannot be allocated a living space", "red")
        # add a new fellow member
        elif person_type == "FELLOW":
            fellow_object = Fellow(person_name)
            self.all_people['fellow'].append(fellow_object)
            cprint("Fellow {} added successfully".format(
                   fellow_object.person_name), "cyan")
            self.allocate_room("OFFICE", fellow_object)
            if want_accomodation == "Y":
                self.allocate_room("LIVINGSPACE", fellow_object)
        elif person_type not in ["STAFF", "FELLOW"]:
            cprint("Invalid person type", "red")

    def remove_person_from_previous_office(self, person_name):

        """ Removes a staff or fellow from the offices they were previously
            located in or from the waiting list if they did not have
            a livingspace """
        for room in self.all_rooms['office']:
            for person in room.room_occupants:
                if person == person_name:
                    room.room_occupants.remove(person_name)
                    cprint("{} sucessfully removed from previous office".format(person_name), "cyan")
                    return
        if person_name in self.waiting_list['office']:
            self.waiting_list['office'].remove(person_name)
            cprint("{} sucessfully removed from waiting list".format(
                   person_name), "cyan")

    def remove_person_from_previous_livingspace(self, person_name):
        """ Removes a fellow from the living spaces they were previously
            located in or from the waiting list if they did not have a
            livingspace """
        for room in self.all_rooms['livingspace']:
            for person in room.room_occupants:
                if person == person_name:
                    room.room_occupants.remove(person_name)
                    cprint("{} sucessfully removed from previous livingspace"
                           .format(person_name), "cyan")
                    return
        if person_name in self.waiting_list['livingspace']:
            self.waiting_list['livingspace'].remove(person_name)
            cprint("{} sucessfully removed from waiting list".format(
                   person_name), "cyan")

    def reallocate_staff(self, person_name, new_room_name):
        """ Reallocate a staff to a different office and rejects allocation to
            a living space """
        try:
            for room in self.all_rooms['office'] + self.all_rooms[
                                                               'livingspace']:
                if room.room_name == new_room_name and room.room_type == "office":
                    for person in room.room_occupants:
                        # checks if person already exists in the new office
                        if person.person_name == person_name:
                            cprint("Person {} does not exist".format(
                                   person_name), "red")
                            return
                            # reallocate a person and call function
                            # remove_person_from_previous_office
                            # to remove the staff from the previous
                            # office or waiting list
                    if len(room.room_occupants) < 6:
                        self.remove_person_from_previous_office(person_name)
                        room.room_occupants.append(person_name)
                        cprint("{} has been reallocated successfully to office {}".format(person_name,
                               new_room_name), "cyan")
                        return
                    else:
                        cprint("Office {} is full, choose another room".format(
                               new_room_name), "red")

                elif room.room_name == new_room_name and room.room_type == "livingspace":
                        cprint("Cannot reallocate a staff member to a living space", "red")
                        return
        except:
            cprint("{} does not exist".format(person_name), "red")

    def reallocate_fellow(self, person_name, new_room_name):
        """ Reallocate a fellow to a different office or living space """
        try:
            for room in self.all_rooms['office'] + self.all_rooms['livingspace']:
                if room.room_name == new_room_name and room.room_type == "office":
                    for person in room.room_occupants:
                        if person == person_name:
                            cprint("{} already exists in the room {}".format(
                                   person_name, new_room_name), "red")
                            return
                    if len(room.room_occupants) < 6:
                        self.remove_person_from_previous_office(person_name)
                        room.room_occupants.append(person_name)
                        cprint("{} has been reallocated successfully to office {}".format(person_name, new_room_name), "cyan")
                        return
                    else:
                        cprint("Office {} is full, choose another room".format(
                               new_room_name), "red")
                        return
                elif room.room_name == new_room_name and room.room_type == "livingspace":
                    for person in room.room_occupants:

                        if person == person_name:
                            cprint("{} already exists in the room {}"
                                   .format(person_name, new_room_name), "red")
                            return
                    if len(room.room_occupants) < 4:
                        self.remove_person_from_previous_livingspace(
                                                                 person_name)
                        room.room_occupants.append(person_name)
                        cprint("{} has been reallocated successfully to livingspace {}".format(person_name,
                               new_room_name), "cyan")
                        return
                    else:
                        cprint("Livingspace {} is full, choose another room".format(new_room_name), "red")
                        return
                else:
                    cprint("The room {} does not exist".format(
                           new_room_name), "red")
        except:
            cprint("{} does not exist".format(person_name), "red")

    def reallocate_person(self, person_name, new_room_name):
        """ Reallocate a person to a different office or living space """
        try:
            for person in self.all_people['staff'] + self.all_people['fellow']:
                if person.person_name == person_name and person.person_type == "staff":
                    self.reallocate_staff(person_name, new_room_name)
                elif person.person_name == person_name and person.person_type == "fellow":
                    self.reallocate_fellow(person_name, new_room_name)
        except:
            cprint("{} does not exist".format(person_name), "red")

    def load_people(self, filename):
        """ Collects details about employees from a .txt file and
            adds them to the system """
        try:
            filepath = 'files/' + filename + '.txt'
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
                    self.add_person(person_type, person_name,
                                    want_accomodation)
        except:
            cprint('That file does not exist...', "red")

    def print_unallocated(self, filename=None):
        """ Prints a list of the people still waiting to be
            allocated into rooms """
        try:
            if filename:
                filepath = 'files/' + filename + '.txt'
                print_unallocated_file = open(filepath, 'w')
                for person in self.waiting_list['office'] + self.waiting_list['livingspace']:
                    print_unallocated_file.write(person.person_name + '\n')
                print_unallocated_file.close()
                cprint('\t\t Printing to {} completed'.format(
                       filepath), "white")
            else:
                for person in self.waiting_list['office'] + self.waiting_list['livingspace']:
                    cprint(person.person_name, "yellow")
        except:
            cprint("An error occured while printing. Please try again", "red")

    def print_room(self, room_name):
        """ print the room occupants in a specified room """
        for room in self.all_rooms['office'] + self.all_rooms['livingspace']:
            try:
                if room.room_name == room_name:
                    if room.room_occupants:
                        cprint('{} NAME: {} \n'.format(room.room_type.upper(),
                               room.room_name), "white")
                        cprint('*'*60, "cyan")
                        cprint(',\t'. join(room.room_occupants), "magenta")
                        print('\n')
                    else:
                            cprint("There are no occupants in room {}"
                                   .format(room.room_name), "red")
                    return
            except:
                cprint("Room {} does not exist".format(room_name), "red")

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
                filepath = 'files/' + filename + '.txt'
                print_allocations_file = open(filepath, 'w')
                print_allocations_file.write("OFFICES...\n")
                for room in self.all_rooms['office']:
                    print_allocations_file.write('\n\t' + room.room_name +
                                                 '\n' + '-' * 60 + '\n')
                    if room.room_occupants:
                        for person in room.room_occupants:
                            print_allocations_file.write('\t' + person + ',')
                    else:
                        print_allocations_file.write("No occupants")
                    print_allocations_file.write('\n\n')
                print_allocations_file.write("LIVINGSPACES...\n")
                for room in self.all_rooms['livingspace']:
                    print_allocations_file.write('\n\t' + room.room_name +
                                                 '\n' + '-' * 60 + '\n')
                    if room.room_occupants:
                        for person in room.room_occupants:
                            print_allocations_file.write(person)
                    else:
                        print_allocations_file.write("No occupants")
                    print_allocations_file.write('\n')
                print_allocations_file.close()
                cprint('\t\t Printing to {} complete'.format(
                       filepath), "white")
            else:
                self.print_office_allocations()
                self.print_livingspace_allocations()
        except:
            cprint("An error occured while printing. Please try again", "red")

    def save_state():
        pass

    def load_state():
        pass
