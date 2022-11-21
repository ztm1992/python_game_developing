import datetime
import tkinter


def time_now():
    d = datetime.datetime.now()
    t = f"{d.hour}:{d.minute}:{d.second}"
    label["text"] = t
    root.after(1000, time_now)


root = tkinter.Tk()
root.geometry("400x200")
root.title("easy timer")
label = tkinter.Label(font=("Times New Roman", 60))
label.pack()
time_now()
root.mainloop()
