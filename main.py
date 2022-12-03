from timetable import *

import numpy as np

def main():
    print('Starting the program')

    # Generate random timetable data
    room_1 = Room("BC410")
    room_2 = Room("BC420")

    room_1.add_booking(RoomBooking(1.5,2.5,4))
    room_1.add_booking(RoomBooking(4,5,2))
    room_2.add_booking(RoomBooking(5,8,1))

    data_tt = {room_1, room_2}

    # Put it inside Timetable object
    tt = Timetable(data_tt)

    # Display data
    tt.display()


if __name__ == '__main__':
    main()