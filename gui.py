import tkinter as tk


class DateEntry(tk.Frame):
    def __init__(self, master, frame_look=None, **look):
        if frame_look is None:
            frame_look = {}
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)
        self.day = tk.StringVar(master)
        self.month = tk.StringVar(master)
        self.year = tk.StringVar(master)
        args = {'relief': tk.FLAT}
        args.update(look)
        self.message = tk.Label(self, text='yyyy/mm/dd', **args)
        self.entry_1 = tk.Entry(self, width=4, textvariable=self.year, **args)
        self.label_1 = tk.Label(self, text='/', **args)
        self.entry_2 = tk.Entry(self, width=2, textvariable=self.month, **args)
        self.label_2 = tk.Label(self, text='/', **args)
        self.entry_3 = tk.Entry(self, width=2, textvariable=self.day, **args)
        self.message.pack(side=tk.TOP)

        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.entry_3.pack(side=tk.LEFT)

        self.entry_1.bind('<KeyRelease>', self._e1_check)
        self.entry_2.bind('<KeyRelease>', self._e2_check)
        self.entry_3.bind('<KeyRelease>', self._e3_check)

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, cont[:-1])

    def _e1_check(self, e):
        cont = self.entry_1.get()
        if len(cont) >= 4:
            self.entry_2.focus()
        if len(cont) > 4 or not cont[-1].isdigit():
            self._backspace(self.entry_1)
            self.entry_1.focus()

    def _e2_check(self, e):
        cont = self.entry_2.get()
        if len(cont) >= 2:
            self.entry_3.focus()
        if len(cont) > 2 or not cont[-1].isdigit():
            self._backspace(self.entry_2)
            self.entry_2.focus()

    def _e3_check(self, e):
        cont = self.entry_3.get()
        if len(cont) > 2 or not cont[-1].isdigit():
            self._backspace(self.entry_3)

    def get(self):
        return self.entry_1.get(), self.entry_2.get(), self.entry_3.get()


class OrbitEntry(tk.Frame):
    def __init__(self, master, frame_look=None, **look):
        if frame_look is None:
            frame_look = {}
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)
        args = {'relief': tk.FLAT}
        args.update(look)
        self.a = tk.StringVar(master)
        self.e = tk.StringVar(master)
        self.i = tk.StringVar(master)
        self.Omega = tk.StringVar(master)
        self.omega = tk.StringVar(master)
        self.Mo = tk.StringVar(master)
        self.entry_1 = tk.Entry(self, width=15, textvariable=self.a, **args)
        self.entry_2 = tk.Entry(self, width=15, textvariable=self.e, **args)
        self.entry_3 = tk.Entry(self, width=15, textvariable=self.i, **args)
        self.entry_4 = tk.Entry(self, width=15, textvariable=self.Omega, **args)
        self.entry_5 = tk.Entry(self, width=15, textvariable=self.omega, **args)
        self.entry_6 = tk.Entry(self, width=15, textvariable=self.Mo, **args)
        self.label_1 = tk.Label(self, text='a (km) ', **args)
        self.label_2 = tk.Label(self, text='e ', **args)
        self.label_3 = tk.Label(self, text='i (deg) ', **args)
        self.label_4 = tk.Label(self, text='Omega (deg)', **args)
        self.label_5 = tk.Label(self, text='w (deg) ', **args)
        self.label_6 = tk.Label(self, text='Mo (deg) ', **args)
        self.label_1.grid(row=1, column=1)
        self.entry_1.grid(row=1, column=2)
        self.label_2.grid(row=2, column=1)
        self.entry_2.grid(row=2, column=2)
        self.label_3.grid(row=3, column=1)
        self.entry_3.grid(row=3, column=2)
        self.label_4.grid(row=4, column=1)
        self.entry_4.grid(row=4, column=2)
        self.label_5.grid(row=5, column=1)
        self.entry_5.grid(row=5, column=2)
        self.label_6.grid(row=6, column=1)
        self.entry_6.grid(row=6, column=2)

        self.entry_1.bind('<KeyRelease>', self._entry1_check)
        self.entry_2.bind('<KeyRelease>', self._entry2_check)
        self.entry_3.bind('<KeyRelease>', self._entry3_check)
        self.entry_4.bind('<KeyRelease>', self._entry4_check)
        self.entry_5.bind('<KeyRelease>', self._entry5_check)
        self.entry_6.bind('<KeyRelease>', self._entry6_check)

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, cont[:-1])

    def _entry1_check(self, e):
        cont = self.entry_1.get()
        if len(cont) >= 15:
            self.entry_2.focus()
        if len(cont) > 15 or (not cont[-1].isnumeric() and not cont[-1] == '.'):
            self._backspace(self.entry_1)
            self.entry_1.focus()

    def _entry2_check(self, e):
        cont = self.entry_2.get()
        if len(cont) >= 15:
            self.entry_3.focus()
        if len(cont) > 15 or (not cont[-1].isnumeric() and not cont[-1] == '.'):
            self._backspace(self.entry_2)
            self.entry_2.focus()

    def _entry3_check(self, e):
        cont = self.entry_3.get()
        if len(cont) >= 15:
            self.entry_4.focus()
        if len(cont) > 15 or (not cont[-1].isnumeric() and not cont[-1] == '.'):
            self._backspace(self.entry_3)
            self.entry_3.focus()

    def _entry4_check(self, e):
        cont = self.entry_4.get()
        if len(cont) >= 15:
            self.entry_5.focus()
        if len(cont) > 15 or (not cont[-1].isnumeric() and not cont[-1] == '.'):
            self._backspace(self.entry_4)
            self.entry_4.focus()

    def _entry5_check(self, e):
        cont = self.entry_5.get()
        if len(cont) >= 15:
            self.entry_6.focus()
        if len(cont) > 15 or (not cont[-1].isnumeric() and not cont[-1] == '.'):
            self._backspace(self.entry_5)
            self.entry_5.focus()

    def _entry6_check(self, e):
        cont = self.entry_6.get()
        if len(cont) >= 15:
            self.entry_1.focus()
        if len(cont) > 15 or (not cont[-1].isnumeric() and not cont[-1] == '.'):
            self._backspace(self.entry_6)
            self.entry_6.focus()

    def get(self):
        return (self.entry_1.get(), self.entry_2.get(), self.entry_3.get(), self.entry_4.get(), self.entry_5.get(),
                self.entry_6.get())
