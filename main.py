import math
import tkinter as tk
from datetime import datetime, timedelta

import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from constants import *
from gui import DateEntry, OrbitEntry
from orbit import Orbit
from planets import Planets_Vec, Earth
from transfer import hohmann_transfer
from utils import is_valid_date

plt.use('TkAgg')
default_day = datetime(year=1957, month=1, day=1)

day_length = 86400  # seconds


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.date_value = datetime(year=1957, month=10, day=4)
        self.arrival_date = datetime(year=1957, month=10, day=4)
        self.f = plt.figure.Figure(figsize=(12, 15), dpi=100)
        self.a = self.f.add_subplot(111, projection='polar')
        self.valid_orbit = False
        self.my_orbit = Orbit()
        self.plot_solar_system()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Frames
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT)
        # Center Frame
        self.my_date = tk.StringVar()
        self.output = tk.StringVar()
        self.current_date = tk.Label(self.center_frame, font=('times', 20, 'bold'), bg='green',
                                     textvariable=self.my_date)
        self.current_date.pack(side=tk.TOP)
        self.my_date.set(self.date_value)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.center_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg(self.canvas, self.center_frame)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Right Frame
        self.request1 = tk.Label(self.right_frame, font=('Helvetica', 20, 'bold'), text="Change the display date below")
        self.request1.pack(side=tk.TOP)
        self.dentry = DateEntry(self.right_frame, font=('Helvetica', 40, tk.NORMAL), border=0)
        self.dentry.pack(side=tk.TOP)
        self.dentry.day.trace("w", self.check_date)
        self.dentry.month.trace("w", self.check_date)
        self.dentry.year.trace("w", self.check_date)
        self.request2 = tk.Label(self.right_frame, font=('Helvetica', 20, 'bold'),
                                 text="Enter the Orbital elements of the\n goal heliocentric orbit below ")
        self.request2.pack(side=tk.TOP)
        self.oentry = OrbitEntry(self.right_frame, font=('Helvetica', 40, tk.NORMAL), border=0)
        self.oentry.pack(side=tk.TOP)

        self.request3 = tk.Label(self.right_frame, font=('Helvetica', 20, 'bold'),
                                 text="Enter the desired arrival date of the satellite")
        self.request3.pack(side=tk.TOP)
        self.dentry2 = DateEntry(self.right_frame, font=('Helvetica', 40, tk.NORMAL), border=0)
        self.dentry2.pack(side=tk.TOP)

        self.results = tk.Label(self.right_frame, font=('Helvetica', 12), bg='red',
                                textvariable=self.output)
        self.results.pack(side=tk.TOP)
        self.submit = tk.Button(self.right_frame, text="Update Orbit", width=10, command=self.update_orbit)
        self.submit.pack(side=tk.TOP)

        self.quit = tk.Button(self.right_frame, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side=tk.TOP)

    def check_date(self, *args):
        day = self.dentry.day.get()
        month = self.dentry.month.get()
        year = self.dentry.year.get()

        if day and month and year:
            day = int(day)
            month = int(month)
            year = int(year)
            date_array = (day, month, year)
            if is_valid_date(d=day, m=month, y=year):
                print("Valid date found!!!")
                self.date_value = datetime(year=date_array[2], month=date_array[1], day=date_array[0])
                print(self.date_value)
                self.my_date.set(self.date_value)
                self.plot_solar_system()
                self.canvas.draw()

            else:
                print("Invalid date :(")
            print(date_array)

    def update_orbit(self):
        a = self.oentry.a.get()
        e = self.oentry.e.get()
        i = self.oentry.i.get()
        Omega = self.oentry.Omega.get()
        omega = self.oentry.omega.get()
        Mo = self.oentry.Mo.get()
        try:
            a = float(a) * 1000
            e = float(e)
            i = math.radians(float(i))
            Omega = math.radians(float(Omega))
            w = math.radians(float(omega))
            Mo = math.radians(float(Mo))
            self.my_orbit = Orbit(a=a, e=e, i=i, Omega=Omega, omega=omega, mo=Mo, mu=mu_sun, name="Goal Orbit")
            self.valid_orbit = True
        except ValueError:
            print("Bad input for orbit parameter")
            self.valid_orbit = False
        day = self.dentry2.day.get()
        month = self.dentry2.month.get()
        year = self.dentry2.year.get()
        if day and month and year:
            day = int(day)
            month = int(month)
            year = int(year)
            date_array = (day, month, year)
            if is_valid_date(d=day, m=month, y=year):
                print("Valid date found!!!")
                self.arrival_date = datetime(year=date_array[2], month=date_array[1], day=date_array[0])
                print(self.arrival_date)
            else:
                print("Invalid date :(")
                self.valid_orbit = False
            print(date_array)
        self.calculate_transfers()
        self.plot_solar_system()
        self.canvas.draw()

    def calculate_transfers(self):
        earth_orbit = Earth
        if self.valid_orbit:
            r_final = (self.my_orbit.a * (1 - self.my_orbit.e * math.cos(self.my_orbit.ecc_anomaly)))
            # Start by calculating a simple hohmann transfer
            (a_trans, t_trans, delta_v_a, delta_v_b, delta_v) = hohmann_transfer(r_initial=earth_orbit.a,
                                                                                 orbit_initial=earth_orbit,
                                                                                 r_final=r_final,
                                                                                 orbit_final=self.my_orbit, mu=mu_sun)
            new_date = self.arrival_date - timedelta(seconds=t_trans)
            output_str = "Model 1: Simple Hohmann Transfer " + "\n" + "Initial delta_v: " + str(
                delta_v_a / 1000) + "(km/s) \n Final delta_v: " + str(
                delta_v_b / 1000) + "(km/s) \n Total Delta_v: " + str(
                delta_v / 1000) + "(km/s) \n Required Launch date from earth orbit: " + str(new_date)
            self.output.set(output_str)

    def plot_solar_system(self):
        mercury_nu = math.radians(333.3721)
        venus_nu = math.radians(88.7083)
        earth_nu = math.radians(358.3110)
        mars_nu = math.radians(79.7596)
        jupiter_nu = math.radians(157.2837)
        saturn_nu = math.radians(152.4320)
        uranus_nu = math.radians(316.3032)
        neptune_nu = math.radians(129.1372)
        pluto_nu = math.radians(287.1723)
        nu_vec = [mercury_nu, venus_nu, earth_nu, mars_nu, jupiter_nu, saturn_nu, uranus_nu, neptune_nu, pluto_nu]
        tdiff = self.date_value - default_day
        print("Date diff " + str(tdiff))
        self.a.cla()
        self.a.set_theta_zero_location("W")
        for (Planet, nu) in zip(Planets_Vec, nu_vec):
            (_, rem) = divmod(tdiff.days * day_length + tdiff.seconds, Planet.period)
            Planet.mo = float('nan')
            Planet.ecc_anomaly = float('nan')
            Planet.nu = nu
            Planet.find_eccentric_anomaly()
            Planet.find_mean_anomaly()
            Planet.propagate(rem)
            Planet.polar_plot(time_step=day_length, fig=self.a, label=Planet.name)
        if self.valid_orbit and self.arrival_date >= self.date_value:
            tdiff = self.arrival_date - self.date_value
            tmp_orbit = self.my_orbit
            print("Satellite Date diff " + str(tdiff))
            (_, rem) = divmod(tdiff.days * day_length + tdiff.seconds, tmp_orbit.period)
            tmp_orbit.propagate(-rem)
            tmp_orbit.polar_plot(time_step=day_length, fig=self.a, label=self.my_orbit.name)
        self.a.legend(bbox_to_anchor=(1, 1),
                      bbox_transform=self.f.transFigure)


if __name__ == '__main__':
    print("Getting started")

    root = tk.Tk()
    app = Application(master=root)

    app.mainloop()
