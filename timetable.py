import datetime
import pickle
from tqdm import tqdm
import json
import os
import re
import random


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
    def __init__(self, id, info, str_start, str_end) -> None:
        self.id = id
        self.info = info
        self.str_start = str_start
        self.str_end = str_end

    def display(self):
        print(self.info, 'between', self.str_start, 'and', self.str_end)

    def get_mins(self):
        format = "%Y-%m-%dT%H:%M:%S"
        start_unix = datetime.datetime.strptime(self.str_start, format).timestamp() 
        end_unix = datetime.datetime.strptime(self.str_end, format).timestamp()
        return start_unix, end_unix 

    def check_conflict(self, other_booking):
        this_start_unix, this_end_unix = self.get_mins()
        other_start_unix, other_end_unix = other_booking.get_mins()
        if this_end_unix <= other_end_unix and this_end_unix > other_start_unix:
            return True
        elif this_start_unix <= other_start_unix and this_end_unix >= other_end_unix:
            return True
        elif other_end_unix <= this_end_unix and other_end_unix > this_start_unix:
            return True
        elif other_start_unix <= this_start_unix and other_end_unix >= this_end_unix:
            return True
        return False


class Timetable:
    def __init__(self) -> None:

        self.rooms = {}
        if not os.path.isfile("./timetable.pkl"):
            print("Hang on a second, we are loading the rooms for each building...")
            
            from selenium import webdriver
            self.browser=webdriver.Safari()
            self.browser.implicitly_wait(10)

            #buildings = self.__get_buildings()
            buildings = ["BC"]
            list_rooms = [room.replace(" ","") for one_building in tqdm(buildings) for room in self.__get_rooms(one_building)]
            #list_rooms = random.sample(list_rooms,100)
            #list_rooms = ["BC410", "BC420"]
            #print(f"\nFun fact: EPFL has {len(list_rooms)} rooms distributed over {len(buildings)} buildings.\n\n")

            for room_id in tqdm(list_rooms):
                self.rooms[room_id] = self.__get_timetable(room_id)

            del self.browser
            
            with open('timetable.pkl', 'wb') as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        else:
            print("Loading available timetable from cache...")
            with open('timetable.pkl', 'rb') as f:
                loaded_obj = pickle.load(f)
            self.rooms = loaded_obj.rooms

    def get_room(self, room_id) -> Room:
        return self.rooms[room_id]

    def get_number_of_reservations(self) -> int:
        counter = 0
        for room_id, room in self.rooms.items():
            counter += len(room.bookings)
        return counter

    def add_room_booking(self, room_id, booking):
        self.rooms[room_id].add_booking(booking)

    def display_room(self, room_id):
        self.rooms[room_id].display()

    def display(self):
        for room_id in self.rooms:
            self.rooms[room_id].display()

    def __get_html_source(self, url) -> str:

        # get source code
        # makes the browser wait if it can't find an element
        self.browser.get(url)
        html = self.browser.page_source

        return html

    def __get_buildings(self) -> list:

        url = "https://plan.epfl.ch/buildings.html"

        # extract plain html file as string
        raw_html = self.__get_html_source(url)

        # set static beginning and end flags of each room specification
        start_string = '">'
        stop_string = '</a>'

        # define a pattern to filter
        pattern = f'{start_string}.*{stop_string}'

        # extract room ids using regex pattern and cutting away unnecessary characters
        buildings = [substring[len(start_string):-len(stop_string)] for substring in re.findall(pattern, raw_html)]

        return buildings

    def __get_rooms(self, building) -> list:

        url = f'https://plan.epfl.ch/buildings/{building}.html'

        # extract plain html file as string
        raw_html = self.__get_html_source(url)

        # set static beginning and end flags of each room specification
        start_string = 'room=='
        stop_string = '">'

        # define a pattern to filter
        pattern = f'{start_string}.*{stop_string}'

        # extract room ids using regex pattern and cutting away unnecessary characters
        rooms = [substring[len(start_string):-len(stop_string)] for substring in re.findall(pattern, raw_html)]
        
        # warning message in case no rooms were found
        if len(rooms) == 0:
            print(f"WARNING: No rooms found for building {building}")

        return rooms

    def __get_timetable(self, room_id):

        url = f'https://ewa.epfl.ch/room/Default.aspx?room={room_id}'

        # extract plain html file as string
        raw_html = self.__get_html_source(url)

        # set static beginning and end flags of events section
        start_string = "v.events = "
        stop_string = ";\nv.hours = "

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
            new_booking = RoomBooking(id=entry["Value"], str_start=entry["Start"], str_end=entry["End"], info=entry["Text"])
            room_obj.add_booking(new_booking)

        return room_obj

if __name__ == "__main__":# start web browser
    table0 = Timetable()
    table0.display()