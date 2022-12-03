from timetable import *
from temperature import *

import matplotlib.pyplot as plt
import numpy as np

def main():
    print('Starting the program')

    # Get room information online
    list_rooms = ["BC410", "BC420"]
    tt = Timetable(list_rooms)

    # Display data
    tt.display()

    # Temperature evolution
    T_cold = 10
    T_hot = 20
    k = 1

    time_span = np.arange(0,20)
    temperature_evolution = TemperatureEvolution()
    temperature_span = temperature_evolution.cooling_law(T_hot, T_cold, k, time_span)
    plt.plot(time_span, temperature_span)
    plt.show()


if __name__ == '__main__':
    main()