import tkinter as tk
from functools import partial


class GUI(tk.Tk):
    def __init__(self, error):
        super(GUI, self).__init__()
        self.geometry("500x200")
        self.setLabel(error)

    def setLabel(self, text):
        tk.Label(text=text).pack()

    def setPositiveButton(self, text, func: partial):
        try_btn = tk.Button(
            master=self,
            text=text,
            command=func
        )
        try_btn.pack()

    def setNegativeButton(self, text):
        close_btn = tk.Button(
            master=self,
            text=text,
            command=self.quit
        )

        close_btn.pack()

    def quit(self):
        self.destroy()

    def start(self):
        self.mainloop()
