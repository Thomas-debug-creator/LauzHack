
from timetable import *
from temperature import *
from heating_regulation_system import *

import numpy as np
from math import floor


def main():
    print('Main simplified')



    # Temperature evolution
    T_min = 15
    temperature_evolution = TemperatureEvolution()
    
    # Make up data for one room
    room_id = "BC420"
    booking_1 = RoomBooking("BC420", "b1", "2022-11-28T09:00:00", "2022-11-28T12:00:00")
    booking_2 = RoomBooking("BC420", "b2", "2022-11-28T12:09:00", "2022-11-28T14:00:00")
    booking_3 = RoomBooking("BC420", "b3", "2022-11-28T15:00:00", "2022-11-28T17:00:00")
    room = Room(room_id)
    room.add_booking(booking_1)
    room.add_booking(booking_2)
    room.add_booking(booking_3)

    room.display()

    # Create heating regulation system
    hrs = HeatingRegulationSystem(room, temperature_evolution)
    # hrs.get_room_occupancy_in_mn()
    # hrs.compute_time_shifts()


    hrs.control_heating()
    hrs.plot_heat_regulation_curve()



if __name__ == '__main__':
    main()