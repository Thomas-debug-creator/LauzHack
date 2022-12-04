from scipy.optimize import fsolve
from timetable import *
from temperature import *
from heating_regulation_system import *

import numpy as np
from math import floor

def compute_warmup_time(T_min, T_heat, T_cool, k_heat, k_cool, T_start, t_cool, t_target):
    e = 2.718

  
    def f_to_optimize(t_star):
        return T_heat - T_min + (T_cool + (T_start - T_cool)*e**(-k_cool*(t_star - t_cool)) - T_heat)*e**(-k_heat*(t_target - t_star))

    t_star_guess = t_target - 5
    sol = fsolve(f_to_optimize, t_star_guess)

    return sol[0]



def main():
    print('Starting the program')

    # # Get room information online
    # list_rooms = ["BC410", "BC420"]
    # tt = Timetable(list_rooms)

    # # Display data
    # tt.display()

    # # Heating regulation system for one room
    # hrs = HeatingRegulationSystem(tt.rooms[list_rooms[0]])
    # hrs.control_heating()
    # hrs.plot_heat_regulation_curve()



    # Temperature evolution
    T_heat = 20
    T_cool = 3
    T_min = 15
    k_heat = 0.2
    k_cool = 0.05
    temperature_evolution = TemperatureEvolution(T_min)
    
    # random time occupancies
    times_occupancy = np.array([1,2,2.25,4,8,12,14,15]) * 60
    T_start = T_cool
    T_end = T_heat

    # Compute the times at which the heater should be switched on and off
    time_shifts = [0]
    t_star = 0

    for i in range(len(times_occupancy)):
        # Compute the times based on previous times and temperatures
        if i % 2 == 0: # heating time
            T_end = T_heat
            t_star = compute_warmup_time(T_min, T_heat, T_cool, k_heat, k_cool, T_start, time_shifts[-1], times_occupancy[i])
        else: # cooling time
            T_end = T_cool
            t_star = compute_warmup_time(T_min, T_cool, T_heat, k_cool, k_heat, T_start, time_shifts[-1], times_occupancy[i])
            # t_star = times_occupancy[i] - 5 # hardcoded for now, should be recomputed

        time_shifts.append(floor(t_star))

        # Simulate for the considered period to get the new starting temperature
        time_span_period, temperature_span_period = temperature_evolution.simulate_heat_transfer_over_period(T_start, T_end, time_shifts[-2], time_shifts[-1])
        T_start = temperature_span_period[-1]

    # Remove the first entry of the time shifts corresponding to the start of the time frame
    time_shifts = np.array(time_shifts[1:])

    # Use the time shifts to simulate the whole evolution
    time_data, temperature_data = temperature_evolution.simulate_varying_heat_transfers_over_period(T_cool, T_heat, time_shifts, times_occupancy)




if __name__ == '__main__':
    main()