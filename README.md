[![Travis branch](https://img.shields.io/travis/daisymacharia/Check-Point-1-Amity-Allocations/develop.svg)]()
[![Coverage Status](https://coveralls.io/repos/github/daisymacharia/Check-Point-1-Amity-Allocations/badge.svg?branch=develop)](https://coveralls.io/github/daisymacharia/Check-Point-1-Amity-Allocations?branch=develop)
# Check-Point-1-Amity-Allocations
A command-line application of a room allocation system for one of Andela’s facilities called Amity. This application allows one to create a list of rooms, add person, load the data stored in the application to a database among other functions.

The building blocks are:
  * Python 3
  * Docopt

## INSTALLATION
These are instructions for setting up Amity Command Line app in development environment.

* prepare directory for project code and virtualenv:

      $ mkdir -p ~/Command_Line_app

      $ cd ~/Command_Line_app
* prepare virtual environment (with virtualenv you get pip, we'll use it soon to install requirements):

      $ virtualenv --python=python3 amity-venv

      $ source amity-venv/bin/activate
* check out project code:

      $ git clone https://github.com/daisymacharia/Check-Point-1-Amity-Allocations

* install requirements into virtualenv:

      $ pip install -r Check-Point-1-Amity-Allocations/requirements.txt

 * Run the application:

       $ python app.py -i

       $ git checkout develop

 ### COMMANDS AVAILABLE
 * create_room <room_type><room_name(s)>

 Creates room(s) where room_type can be either livingspace or office space.
 The user can enter one or more room names

       $ (Amity)create_room office Hogwarts Camelot
       $ Office HOGWARTS created successfully
       $ Office CAMELOT created successfully

       $ (Amity)create_room livingspace  Cotonou Accra
       $ Livingspace COTONOU created successfully
       $ Livingspace ACCRA created successfully

 * add_person <person_type> <first_name> <last_name> [want_accomodation]

  Adds a person to the system and allocates the person to a random room. Accomodation is optional for fellows but staff can get  allocated to a living space. Both fellow and staff get office allocations.

       $ (Amity)add_person fellow Daisy Macharia y
       $ Fellow DAISY MACHARIA ID: F-4340879256 added successfully

 * print_allocations [<filename>]

 This can print to a file or on the screen. For file output use the command :

       $ (Amity)print_allocations allocations

       this will print to a allocations.txt file.

 * reallocate_person <person_identifier> <new_room_name>

 ###### Constraints:

        * can only move allocate person to room of same type i.e office to office and living space to living space
        * the new room should have at least one vacant space
        * staff cannot be relocated to living spaces

Also, if the person was not allocated previously, they will be allocated to the new room and deleted from the list of unallocated people if they missed a room of the same type as the new room.

       $ (Amity)reallocate_person F-4340879256 camelot
       $ DAISY MACHARIA has been reallocated successfully...
       
These are some of the commands available in amity allocation. Below is a link to a Demo video for all the commands available.
[![asciicast](https://asciinema.org/a/aji5ojsoazo3grjru8zx7igr5.png)](https://asciinema.org/a/aji5ojsoazo3grjru8zx7igr5)

