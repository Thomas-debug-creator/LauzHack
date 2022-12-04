import matplotlib.pyplot as plt
import numpy as np
import datetime
from timetable import *


class HeatingRegulationSystem:

    def __init__(self, room, T_min=10, T_hot=20, warmup=15, cooldown=5) -> None:
        self.room = room 
        self.T_min = T_min
        self.T_hot = T_hot
        self.warmup = warmup                             # minutes takes to attain desired temperature
        self.cooldown = cooldown                             # minutes takes to attain desired temperature
        self.heat_regulation_curve = {} 

    def get_time_standard(self, room_booking):
        format  = "%Y-%m-%dT%H:%M:%S"
        start = datetime.datetime.strptime(room_booking.str_start, format)
        end = datetime.datetime.strptime(room_booking.str_end, format)
        return start, end

    def convert_to_minutes(self, time):
        return time.hour*60 + time.minute

    def control_heating(self):

        for i in range(len(self.room.bookings)):

            # Get time in UNIX format
            t_start_unix, t_end_unix = self.room.bookings[i].get_mins()

            # Get time in standard format
            start, end = self.get_time_standard(self.room.bookings[i])

            key = 'Room: ' + self.room.id + '  |  Date: ' + datetime.datetime.fromtimestamp(t_start_unix).strftime("%d %b, %Y")
            if key not in self.heat_regulation_curve.keys():
                self.heat_regulation_curve[key] = np.zeros((24*60))

            self.heat_regulation_curve[key][int(self.convert_to_minutes(start) - self.warmup) : int(self.convert_to_minutes(end) - self.cooldown)] = 1
               
        return self.heat_regulation_curve

    def plot_heat_regulation_curve(self):

        xlims = (0, 24*60)
        ylims = (-0.03, 1.03)

        for i in self.heat_regulation_curve.keys():
            plt.figure()
            plt.plot(self.heat_regulation_curve[i])
            plt.title(str(i))
            plt.xticks(np.arange(0, xlims[1]+60, 60), labels=np.arange(0, 25))
            plt.xlabel('Time (Hours)')
            plt.xlim(xlims); plt.ylim(ylims)
            plt.show()

        week_curve = []
        for key in self.heat_regulation_curve.keys():
            week_curve.append(self.heat_regulation_curve[key])
        week_curve = np.array(week_curve).reshape(7*24*60)

        plt.figure()
        plt.plot(week_curve)
        plt.title('Weekly View  |  ' + 'Room: ' + self.room.id)
        plt.xticks(np.arange(0, xlims[1]*8, xlims[1]), labels=np.arange(0, 8))
        for j in range(7):
            plt.vlines(x=xlims[1]*j, ymin=ylims[0], ymax=ylims[1], linewidth=1., color='0.8', linestyles='dashed')
        plt.xlim(0, xlims[1]*7); plt.ylim(ylims)
        plt.xlabel('Day')
        plt.show()