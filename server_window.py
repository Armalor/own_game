from tkinter import *
from tkinter import ttk

root = Tk()
root.title("SERVER")
root.geometry("1024x768")


root.rowconfigure(index=0, weight=1)
root.columnconfigure(index=0, weight=8)
canvas = Canvas(bg="white", height=45, width=45)
canvas.grid(row=0, column=0, columnspan=8, sticky=NSEW)
text1 = canvas.create_text(512, 35, text=f'Подключения:', fill='black', font="Arial 14")

for r in range(1, 3):
    root.rowconfigure(index=r, weight=1)
    for c in range(8):
        root.columnconfigure(index=c, weight=1)

root.rowconfigure(index=4, weight=32)


for r in range(1, 3):
    for c in range(8):
        canvas = Canvas(bg="#c0c0c0", height=45, width=45)
        canvas.grid(row=r, column=c, sticky=NSEW)

# стандартная кнопка
btn = ttk.Button(text="Button", width=150)
btn.grid(row=4, column=0, columnspan=8)

root.mainloop()
