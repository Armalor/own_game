from tkinter import *
from tkinter import ttk

root = Tk()
root.title("SERVER")
root.geometry("800x600")

# стандартная кнопка
btn = ttk.Button(text="Button", width=150)
btn.pack(fill=BOTH, expand=1)

root.mainloop()