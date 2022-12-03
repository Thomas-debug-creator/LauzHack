import numpy as np
import matplotlib.pyplot as plt

class TemperatureEvolution:
    def __init__(self, T_min) -> None:
        self.T_min = T_min

    def heat_transfer(self, T_start, T_end, t_start, t_end, k):
        return T_end + (T_start - T_end)*np.exp(-k*(t_end-t_start))

    def cooling_law(self, T_start, T_end, t_start, t_end):
        k = 0.05
        return self.heat_transfer(T_start, T_end, t_start, t_end, k)

    def heating_law(self, T_start, T_end, t_start, t_end):
        k = 0.2
        return self.heat_transfer(T_start, T_end, t_start, t_end, k)

    def simulate_heat_transfer_over_period(self, T_start, T_end, t_start, t_end, nb_points = 100): 
        # Choose heat transfer function
        heat_transfer_fct = self.cooling_law if T_end < T_start else self.heating_law

        # Create time and temperature vectors
        time_span = np.linspace(t_start, t_end, nb_points)
        temperature_span = np.zeros_like(time_span)

        # Set up original temperature
        temperature_span[0] = T_start

        # Simulate for the whole time period
        for i in range(len(time_span) - 1):
            temperature_span[i+1] = heat_transfer_fct(temperature_span[i], T_end, time_span[i], time_span[i+1])

        return time_span, temperature_span

    def simulate_varying_heat_transfers_over_period(self, T_cool, T_heat, time_shifts, times_occupancy):
        # This function simulates the temperature variations when switching the heater on and off over a period of time

        # time_shifts = np.concatenate(time_shifts, times_occupancy[-1])
        # Prepare containers for the time and temperature data series
        time_data= np.array([0])
        temperature_data = np.array([T_cool])

        temperature_shifts = [T_cool] # for visualization purposes

        last_time = 24*60
        time_shifts = np.append(time_shifts, last_time)

        # Loop over all time changes 
        for i in range(len(time_shifts)-1):
            # Get start and end times for the heat dynamics
            t_start = time_shifts[i]
            t_end = time_shifts[i+1]

            # Get starting and target temperatures
            T_start = temperature_data[-i]
            if i % 2 == 0:
                T_end = T_heat
            else:
                T_end = T_cool

            temperature_shifts.append(T_end)

            # Simulate the temperature change over this time period
            time_span_i, temperature_span_i = self.simulate_heat_transfer_over_period(T_start, T_end, t_start, t_end)
            
            # Put it inside the containers
            time_data = np.concatenate((time_data, time_span_i))
            temperature_data = np.concatenate((temperature_data, temperature_span_i))

        # Plot the results
        self.plot_simulated_temperature_over_periode(time_data, temperature_data, time_shifts, temperature_shifts, times_occupancy)

        return time_data, temperature_data

    
    def plot_simulated_temperature_over_periode(self, time_data, temperature_data, time_shifts, temperature_shifts, times_occupancy):
        plt.plot(time_data, temperature_data, 'darkorange', label='Temperature')
        plt.plot(time_data, self.T_min*np.ones_like(time_data), 'g--', label='Minimum temperature')
        plt.plot(time_shifts[1::2], temperature_shifts[1::2], 'b*', label='Switch off')
        plt.plot(time_shifts[::2], temperature_shifts[::2], 'r*', label='Switch on')
        for t in times_occupancy:
            plt.axvline(t, color = 'k', linestyle = 'dotted')
        plt.xlabel('Time [mn]')
        plt.ylabel('Temperature [°Celsius]')
        plt.title('Temperature change in one room over one day')
        plt.legend()
        plt.show()



if __name__ == '__main__':
    # Test case for temperature changes in one room based on a temperature schedule in the heat regulation system
    T_heat = 20
    T_cool = 10
    T_min = 15

    times_occupancy = np.array([1,2,3,4,5,6, 12,13]) * 60
    time_shifts = times_occupancy - 15
    temperature_evolution = TemperatureEvolution(T_min)

    time_data, temperature_data = temperature_evolution.simulate_varying_heat_transfers_over_period(T_cool, T_heat, time_shifts, times_occupancy)
