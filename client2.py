from tkinter import *
from tkinter import ttk

from client import click

if __name__ == '__main__':
    TEAM_NUMBER = 2

    def finish():
        root.destroy()  # ручное закрытие окна и всего приложения
        print("Закрытие приложения")

    root = Tk()
    root.title(f"Team #{TEAM_NUMBER}")
    root.geometry("1024x768")
    root.iconbitmap(default="favicon.ico")
    root.protocol("WM_DELETE_WINDOW", finish)
    # root.attributes("-fullscreen", True)

    canvas_ping = Canvas(bg="white", height=45)
    canvas_ping.pack(anchor='n', expand=True, fill=X)

    btn = ttk.Button(text="Find server...", command=lambda: click(canvas_ping))
    btn.pack(anchor=CENTER, expand=True)

    root.mainloop()