class Room(object):
    def __init__(self, room_name, room_type, capacity):
        self.capacity = capacity
        self.room_name = room_name
        self.room_type = room_type
        self.room_occupants = []


class LivingSpace(Room):
    def __init__(self, room_name):
        # overrides the room_type and capacity
        super(LivingSpace, self).__init__(room_name, room_type="livingspace",
                                          capacity=4)

class Office(Room):
    def __init__(self, room_name):
        
        super(Office, self).__init__(room_name, room_type="office", capacity=6)
