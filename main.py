
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
    list_rooms = ["BC333", "BC329"]
    table0 = Timetable()
    table0.display()

    for room_id in list_rooms:
        room = table0.rooms[room_id]
        # Create heating regulation system
        hrs = HeatingRegulationSystem(room, temperature_evolution)

        # Apply it and plot the regulation curve
        hrs.control_heating()
        print(hrs.time_shifts)
        # hrs.plot_heat_regulation_curve()


        # Plot the temperature in one room 
        temperature_evolution.simulate_varying_heat_transfers_over_period(T_cool, T_heat, hrs.time_shifts, hrs.times_occupancy)



if __name__ == '__main__':
    main()