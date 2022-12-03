import requests
import json


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
    def __init__(self, id, info, t_start, t_end) -> None:
        self.id = id
        self.info = info
        self.t_start = t_start
        self.t_end = t_end

    def display(self):
        print(self.info, 'between', self.t_start, 'and', self.t_end)

    # TODO: check format of Start/End time if this still works
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
        self.rooms = {}
        for room_id in list_rooms:
            self.rooms[room_id] = self.__get_timetable(room_id)

    def get_room(self, room_id):
        return self.rooms[room_id]

    def add_room_booking(self, room_id, booking):
        self.rooms[room_id].add_booking(booking)

    def display_room(self, room_id):
        self.rooms[room_id].display()

    def display(self):
        for room_id in self.rooms:
            self.rooms[room_id].display()

    def __get_timetable(self, room_id):

        url = f'https://ewa.epfl.ch/room/Default.aspx?room={room_id}'

        # get response
        x = requests.get(url)

        # extract plain html file as string
        raw_html = x.text

        # set static beginning and end flags of events section
        start_string = "v.events = "
        stop_string = ";\r\nv.hours ="

        # check if start_string is present in HTML
        if raw_html.count(start_string) != 1 or raw_html.count(stop_string) != 1:
            raise ValueError("Events could not be extracted properly")

        # cut-out events
        events = raw_html.split(start_string)[1].split(stop_string)[0]

        # define strings to be removed
        unwanted_strings = ["<br>", "\n", "\r", "\\"]

        # replace unwanted strings like linebreak
        for substring in unwanted_strings:
            events = events.replace(substring, "")

        #convert string to json object
        json_object = json.loads(events)

        # preparing return data type
        room_obj = Room(room_id)

        # adding bookings to room
        for entry in json_object:
            new_booking = RoomBooking(id=entry["Value"], t_start=entry["Start"], t_end=entry["End"], info=entry["Text"])
            room_obj.add_booking(new_booking)

        return room_obj

if __name__ == "__main__":
    list_rooms = ["BC410", "BC411"]
    table0 = Timetable(list_rooms)
    table0.display()