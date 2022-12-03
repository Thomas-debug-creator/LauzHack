from timetable import *
from temperature import *
from heating_regulation_system import *

import matplotlib.pyplot as plt
import numpy as np

def main():
    print('Starting the program')

    # Generate random timetable data
    room_1 = Room("BC410")
    room_2 = Room("BC420")

    room_1.add_booking(RoomBooking("BC410","U",1.5,2.5))
    room_1.add_booking(RoomBooking("BC410","U",4,5))
    room_2.add_booking(RoomBooking("BC410","U",5,8))

    # Get room information online
    list_rooms = ["BC410", "BC420"]
    tt = Timetable(list_rooms)

    # Display data
    tt.display()

    # Temperature evolution
    T_cold = 10
    T_hot = 20
    k = 1

    # time_span = np.arange(0,20)
    # temperature_evolution = TemperatureEvolution()
    # temperature_span = temperature_evolution.cooling_law(T_hot, T_cold, k, time_span)
    # plt.plot(time_span, temperature_span)
    # plt.show()

    hrs = HeatingRegulationSystem(room_1)
    hrs.control_heating()
    hrs.plot_heat_regulation_curve()



if __name__ == '__main__':
    main()