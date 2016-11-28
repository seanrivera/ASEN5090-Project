import tkinter as tk
from datetime import datetime

import matplotlib as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from gui import DateEntry
from utils import is_valid_date

plt.use('TkAgg')


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.date_value = datetime(year=1957, month=10, day=4)
        self.f = plt.figure.Figure(figsize=(5, 4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.t = np.arange(0.0, 3.0, 0.01)
        self.s = np.sin(2 * np.pi * self.t)
        self.a.plot(self.t, self.s)
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
        self.request1 = tk.Label(self.right_frame, font=('times', 20, 'bold'), text="Change the date below")
        self.request1.pack(side=tk.TOP)

        self.dentry = DateEntry(self.right_frame, font=('Helvetica', 40, tk.NORMAL), border=0)
        self.dentry.pack(side=tk.TOP)
        self.dentry.day.trace("w", self.check_date)
        self.dentry.month.trace("w", self.check_date)
        self.dentry.year.trace("w", self.check_date)

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
                self.a.cla()
                s = np.sin(day * np.pi * self.t)
                self.a.plot(self.t, s)
                self.canvas.draw()
                self.my_date.set(self.date_value)
            else:
                print("Invalid date :(")
            print(date_array)


if __name__ == '__main__':
    print("Getting started")

    root = tk.Tk()
    app = Application(master=root)

    app.mainloop()
