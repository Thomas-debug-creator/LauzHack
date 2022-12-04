
from timetable import *
from temperature import *
from heating_regulation_system import *

import numpy as np
from math import floor


def main():
    print('Main simplified')



    # Temperature evolution
    T_min = 15
    T_cool = 3
    T_heat = 20
    temperature_evolution = TemperatureEvolution()
    
    # Make up data for one room
    room_id = "BC420"
    booking_1 = RoomBooking("BC420", "b1", "2022-11-28T09:00:00", "2022-11-28T12:00:00")
    booking_2 = RoomBooking("BC420", "b2", "2022-11-28T12:09:00", "2022-11-28T14:00:00")
    booking_3 = RoomBooking("BC420", "b3", "2022-11-28T15:00:00", "2022-11-28T23:59:00")
    booking_4 = RoomBooking("BC420", "b4", "2022-12-01T00:09:00", "2022-12-01T12:00:00")
    booking_5 = RoomBooking("BC420", "b5", "2022-12-01T15:09:00", "2022-12-01T18:00:00")
    booking_6 = RoomBooking("BC420", "b6", "2022-12-01T19:00:00", "2022-12-01T19:30:00")
    room = Room(room_id)
    room.add_booking(booking_1)
    room.add_booking(booking_2)
    room.add_booking(booking_3)
    room.add_booking(booking_4)
    room.add_booking(booking_5)
    room.add_booking(booking_6)


    # Create heating regulation system
    hrs = HeatingRegulationSystem(room, temperature_evolution)

    # Apply it and plot the regulation curve
    hrs.control_heating()
    hrs.plot_heat_regulation_curve()


    # Plot the temperature in one room 
    temperature_evolution.simulate_varying_heat_transfers_over_period(T_cool, T_heat, hrs.time_shifts, hrs.times_occupancy)



if __name__ == '__main__':
    main()