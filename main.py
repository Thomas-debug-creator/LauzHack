from timetable import *

import numpy as np

def main():
    print('Starting the program')

    # Generate random timetable data
    nb_rooms = 2
    data_tt = np.random.randint(-2,5,(nb_rooms,24))
    data_tt[data_tt < 0] = 0

    # Put it inside Timetable object
    tt = Timetable(data_tt)

    # Display data
    print(tt.data)


if __name__ == '__main__':
    main()