import matplotlib.pyplot as plt
import numpy as np
import datetime
from timetable import *
from temperature import *
from math import floor


class HeatingRegulationSystem:

    def __init__(self, room, temperature_evolution, T_cool = 3, T_heat = 20) -> None:
        self.room = room 
        self.temperature_evolution = temperature_evolution
        self.heat_regulation_curve = {} 
        self.T_cool = T_cool
        self.T_heat = T_heat

    def get_time_standard(self, room_booking):
        format  = "%Y-%m-%dT%H:%M:%S"
        start = datetime.datetime.strptime(room_booking.str_start, format)
        end = datetime.datetime.strptime(room_booking.str_end, format)
        return start, end

    def convert_to_minutes(self, time):
        return time.hour*60 + time.minute

    def get_room_occupancy_in_mn(self):
        times_occupancy = []
        for i in range(len(self.room.bookings)):

            # Get time in standard format
            start, end = self.get_time_standard(self.room.bookings[i])

            # Get times in minute format
            start_time_mn = self.convert_to_minutes(start)
            end_time_mn = self.convert_to_minutes(end)

            times_occupancy.append(start_time_mn)
            times_occupancy.append(end_time_mn)

        self.times_occupancy = np.array(times_occupancy)

    def compute_time_shifts(self):
        # Assume the first shits is a switch-on (i.e we start heating)
        T_start = self.T_cool
        T_end = self.T_heat

        time_shifts = [0]
        t_star = 0

        for i in range(len(self.times_occupancy)):
            # Compute the times based on previous times and temperatures
            if i % 2 == 0: # heating time
                T_end = self.T_heat
                t_star = temperature_evolution.compute_warmup_time(self.T_heat, self.T_cool, T_start, time_shifts[-1], self.times_occupancy[i])
            else: # cooling time
                T_end = self.T_cool
                t_star = temperature_evolution.compute_cooldown_time(self.T_heat, self.T_cool, T_start, time_shifts[-1], self.times_occupancy[i])

            time_shifts.append(floor(t_star))

            # Simulate for the considered period to get the new starting temperature
            time_span_period, temperature_span_period = temperature_evolution.simulate_heat_transfer_over_period(T_start, T_end, time_shifts[-2], time_shifts[-1])
            T_start = temperature_span_period[-1]

        #    Remove the first entry of the time shifts corresponding to the start of the time frame
        self.time_shifts = np.array(time_shifts[1:])



    def control_heating(self):
        self.get_room_occupancy_in_mn()
        self.compute_time_shifts()

        for i in range(len(self.room.bookings)):

            # Get time in UNIX format
            t_start_unix, t_end_unix = self.room.bookings[i].get_mins()

            # Get time in standard format
            start, end = self.get_time_standard(self.room.bookings[i])

            # Compute warmump and cooldown times for this period
            warmup_time = self.time_shifts[2*i]
            cooldown_time = self.time_shifts[2*i + 1]

            key = 'Room: ' + self.room.id + '  |  Date: ' + datetime.datetime.fromtimestamp(t_start_unix).strftime("%d %b, %Y")
            if key not in self.heat_regulation_curve.keys():
                self.heat_regulation_curve[key] = np.zeros((24*60))

            self.heat_regulation_curve[key][int(self.convert_to_minutes(start) - warmup_time) : int(self.convert_to_minutes(end) - cooldown_time)] = 1
               
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