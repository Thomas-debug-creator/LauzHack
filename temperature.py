import numpy as np
import matplotlib.pyplot as plt

class TemperatureEvolution:
    def __init__(self) -> None:
        pass

    def heat_transfer(self, T_start, T_end, t_start, t_end, k):
        return T_end + (T_start - T_end)*np.exp(-k*(t_end-t_start))

    def cooling_law(self, T_start, T_end, t_start, t_end):
        k = 0.01
        return self.heat_transfer(T_start, T_end, t_start, t_end, k)

    def heating_law(self, T_start, T_end, t_start, t_end):
        k = 0.1
        return self.heat_transfer(T_start, T_end, t_start, t_end, k)

    def simulate_heat_transfer_over_period(self, T_start, T_end, t_start, t_end, mode, nb_points = 100): # mode = 0 (cooling) or 1 (heating)
        # Choose heat transfer function
        heat_transfer_fct = self.cooling_law if mode == 0 else self.heating_law

        # Create time and temperature vectors
        time_span = np.linspace(t_start, t_end, nb_points)
        temperature_span = np.zeros_like(time_span)

        # Set up original temperature
        temperature_span[0] = T_start

        # Simulate for the whole time period
        for i in range(len(time_span) - 1):
            temperature_span[i+1] = heat_transfer_fct(temperature_span[i], T_end, time_span[i], time_span[i+1])

        return time_span, temperature_span

    
    



if __name__ == '__main__':
    T_heat = 20
    T_cool = 15
    T_room = 10
    t_start_heating = 0
    t_end_heating = 60
    t_start_cooling = 60
    t_end_cooling = 200

    temperature_evolution = TemperatureEvolution()
    time_span_heating, temperature_span_heating = temperature_evolution.simulate_heat_transfer_over_period(T_room, T_heat, t_start_heating, t_end_heating, 1)
    time_span_cooling, temperature_span_cooling = temperature_evolution.simulate_heat_transfer_over_period(temperature_span_heating[-1], T_cool, t_start_cooling, t_end_cooling, 0)

    time_span = np.concatenate((time_span_heating, time_span_cooling))
    temperature_span = np.concatenate((temperature_span_heating, temperature_span_cooling))

    plt.plot(time_span, temperature_span)
    plt.xlabel('Time [mn]')
    plt.ylabel('Temperature')
    plt.show()
