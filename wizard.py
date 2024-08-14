import tkinter as tk
from tkinter import ttk


class Wizard(tk.Tk):
   def __init__(self, *args, **kwargs):
      tk.Tk.__init__(self, *args, **kwargs)

      self.title("Creating a Wizard in tkinter")
      self.geometry("720x250")

      # Create a container to hold wizard frames
      self.container = ttk.Frame(self)
      self.container.pack(side="top", fill="both", expand=True)
      self.container.grid_rowconfigure(0, weight=1)
      self.container.grid_columnconfigure(0, weight=1)

      self.frames = {}

      # Define wizard steps
      steps = [Step1, Step2, Step3]

      for Step in steps:
         frame = Step(self.container, self)
         self.frames[Step] = frame
         frame.grid(row=0, column=0, sticky="nsew")

      self.show_frame(Step1)

   def show_frame(self, cont):
      frame = self.frames[cont]
      frame.tkraise()


class Step1(ttk.Frame):
   def __init__(self, parent, controller):
      ttk.Frame.__init__(self, parent)
      label = ttk.Label(self, text="Step 1")
      label.pack(pady=10, padx=10)
      button = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Step2))
      button.pack()


class Step2(ttk.Frame):
   def __init__(self, parent, controller):
      ttk.Frame.__init__(self, parent)
      label = ttk.Label(self, text="Step 2")
      label.pack(pady=10, padx=10)
      button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Step1))
      button1.pack()
      button2 = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Step3))
      button2.pack()


class Step3(ttk.Frame):
   def __init__(self, parent, controller):
      ttk.Frame.__init__(self, parent)
      label = ttk.Label(self, text="Step 3")
      label.pack(pady=10, padx=10)
      button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Step2))
      button1.pack()
      button2 = ttk.Button(self, text="Finish", command=self.finish)
      button2.pack()

   def finish(self):
      print("Wizard finished!")


if __name__ == "__main__":
   app = Wizard()
   app.geometry("300x250+400+200")
   app.mainloop()