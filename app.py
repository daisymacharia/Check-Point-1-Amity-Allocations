"""

This example uses docopt with the built in cmd module to demonstrate an

interactive command application.

Usage:
    app create_room <room_type> <room_name>...
    app add_person <person_type> <first_name> <last_name> [<want_accomodation>]
    app print_room <room_name>
    app load_people <file_name>
    app print_unallocated [<filename>]
    app reallocate_person <person_identifier> <new_room_name>
    app print_allocated [<filename>]
    app save_state <sqlite_database>
    app load_state <sqlite_database>
    app delete_person <person_identifier>
    app delete_room <room_name>
    app (-i | --interactive)
    app (-h | --help)

Options:
    -i, --interactive  Interactive Mode
    -o, --output  Save to a txt file
    -h, --help  Show this screen and exit.

"""

import sys
import cmd

from docopt import docopt, DocoptExit
from pyfiglet import Figlet, figlet_format
from termcolor import colored, cprint
from amity.Controller.amity import Amity
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))



def docopt_cmd(func):
    """This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action. """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:

            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print(colored('Invalid Command!', "red"))
            print(e)
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return
        return func(self, opt)

    fn.__name__ = func.__name__

    fn.__doc__ = func.__doc__

    fn.__dict__.update(func.__dict__)

    return fn


class Amity(cmd.Cmd):

    amity = Amity()
    cprint(figlet_format("AMITY", font="nipples"), "cyan", attrs=['bold'])

    prompt = '(Amity)'
    file = None
    print(__doc__)

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_name>..."""
        room_type = args['<room_type>'].upper()
        for room_name in args['<room_name>']:
            self.amity.create_room(room_type, room_name.upper())

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <person_type> <first_name> <last_name>
           [<want_accomodation>]"""
        person_type = args['<person_type>'].upper()
        first_name = args['<first_name>'].upper()
        last_name = args['<last_name>'].upper()
        person_name = first_name + " " + last_name
        if args['<want_accomodation>']:
            want_accomodation = args['<want_accomodation>'].upper()
        else:
            want_accomodation = "N"
        self.amity.add_person(person_type, person_name, want_accomodation)

    @docopt_cmd
    def do_reallocate_person(self, args):

        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        p_id = args['<person_identifier>']
        new_room_name = args['<new_room_name>'].upper()
        self.amity.reallocate_person(p_id, new_room_name)

    @docopt_cmd
    def do_print_room(self, arg):

        """Usage: print_room <room_name>"""
        room_name = arg['<room_name>'].upper()
        self.amity.print_room(room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""
        filename = arg['<file_name>']
        self.amity.load_people(filename)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [<filename>]"""
        filename = arg['<filename>'] or None
        self.amity.print_unallocated(filename)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocated [<filename>]"""
        filename = arg['<filename>'] or None
        self.amity.print_allocations(filename)

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage: save_state <sqlite_database> """
        self.amity.save_state(arg['<sqlite_database>'])

    @docopt_cmd
    def do_load_state(self, arg):
        """ Usage: load_state <sqlite_database> """
        self.amity.load_state(arg['<sqlite_database>'])

    @docopt_cmd
    def do_delete_person(self, arg):
        """Usage: delete_person <first_name> <last_name>"""
        p_id = arg['<person_identifier>']
        self.amity.delete_person(p_id)

    @docopt_cmd
    def do_delete_room(self, args):
        """Usage: delete_room <room_name>"""
        room_name = args['<room_name>'].upper()
        self.amity.delete_person(room_name)

    def do_quit(self, args):

        """Quits out of Interactive Mode."""

        print('Good Bye!')

        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:

    Amity().cmdloop()

print(opt)
