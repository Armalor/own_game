from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Client")
root.geometry("300x300")

canvas1 = Canvas(bg="white", width=250, height=50)
canvas1.pack(anchor=CENTER, expand=1)

# canvas2 = Canvas(bg="white", width=250, height=50)
#
# canvas2.pack(anchor=CENTER, expand=1)
#
# canvas3 = Canvas(bg="white", width=250, height=50)
# canvas3.pack(anchor=CENTER, expand=1)

# canvas1.create_line(10, 10, 200, 50)


# def entered(event):
#     btn["text"] = "Entered"
#
#
# def left(event):
#     btn["text"] = "Left"


def click():
    canvas1["bg"] = "green"
    if not hasattr(click, 'clicked'):
        # click.text1 = canvas1.create_text(5, 10, anchor=NW, text="ping: 0.0011", fill="#ffffff", font="Arial 14")
        click.clicked = True
    # else:
       # canvas1.delete(click.text1)

    btn["text"] = "Connected!"


    # canvas2["bg"] = "yellow"
    # canvas2.create_text(5, 10, anchor=NW, text="ping: 0.0011", fill="#ff0000", font="Arial 14")
    #
    # canvas3["bg"] = "red"
    # canvas3.create_text(5, 10, anchor=NW, text="ping: 0.0011", fill="#0000aa", font="Arial 14")


btn = ttk.Button(text="Find server...", command=click)
btn.pack(anchor=CENTER, expand=1)

# btn.bind("<Enter>", entered)
# btn.bind("<Leave>", left)

root.mainloop()