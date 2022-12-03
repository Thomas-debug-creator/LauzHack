import matplotlib.pyplot as plt
import numpy as np

class HeatingRegulationSystem:

    def __init__(self, room, T_min=15, T_ideal=25) -> None:
        self.room = room 
        self.T_min = T_min
        self.T_ideal = T_ideal
        self.heat_regulation_curve = np.zeros((24*60))   # 1-minute quantization
    
    def control_heating(self):
        for i in range(len(self.room.bookings)):
            t_start, t_end = self.room.bookings[i].get_mins()

            self.heat_regulation_curve[int(t_start):int(t_end)] = 1

        return self.heat_regulation_curve

    def plot_heat_regulation_curve(self):
        plt.figure()
        plt.plot(self.heat_regulation_curve)
        plt.show()