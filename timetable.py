class Room:
    def __init__(self, id) -> None:
        self.id = id
        self.bookings = []

    def add_booking(self, new_booking):
        conflict = False
        for booking in self.bookings:
            if booking.check_conflict(new_booking):
                conflict = True
                break
        if not conflict:
            self.bookings.append(new_booking)
        else:
            print("WARNING : cannot add the booking")
            new_booking.display()
            print("because of conflicts")

    def display(self):
        print('Room', self.id, ': ')
        for booking in self.bookings:
            booking.display()

    

class RoomBooking:
    def __init__(self, t_start, t_end, nb_people) -> None:
        self.t_start = t_start
        self.t_end = t_end
        self.nb_people = nb_people

    def display(self):
        print(self.nb_people, 'people between', self.t_start, 'and', self.t_end)

    def check_conflict(self, other_booking):
        if self.t_end <= other_booking.t_end and self.t_end > other_booking.t_start:
            return True
        elif self.t_start <= other_booking.t_start and self.t_end >= other_booking.t_end:
            return True
        elif other_booking.t_end <= self.t_end and other_booking.t_end > self.t_start:
            return True
        elif other_booking.t_start <= self.t_start and other_booking.t_end >= self.t_end:
            return True
        return False


class Timetable:
    def __init__(self, list_rooms) -> None:
        self.rooms = {room.id: room for room in list_rooms}

    def get_room(self, room_id):
        return self.rooms[room_id]

    def add_room_booking(self, room_id, booking):
        self.rooms[room_id].add_booking(booking)

    def display_room(self, room_id):
        self.rooms[room_id].display()

    def display(self):
        for room_id in self.rooms:
            self.rooms[room_id].display()