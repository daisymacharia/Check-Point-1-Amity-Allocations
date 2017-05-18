class Person (object):

    def __init__(self, person_name, person_type, allocate_living_space="N"):
        self.person_name = person_name
        self.person_type = person_type


class Fellow(Person):
    def __init__(self, person_name):
        #overrides the person_type
        super(Fellow, self).__init__(person_name, "fellow")


class Staff(Person):
    def __init__(self, person_name):
        #overrides the person_type
        super(Staff, self).__init__(person_name, "staff")
