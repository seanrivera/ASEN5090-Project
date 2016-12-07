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
