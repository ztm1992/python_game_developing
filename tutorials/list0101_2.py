import tkinter


def key_down(e):
    key_c = e.keycode
    label1["text"] = "keykode: " + str(key_c)
    key_s = e.keysym
    label2["text"] = "keysym: " + str(key_s)


root = tkinter.Tk()
root.geometry("400x200")
root.title("key input")
root.bind("<KeyPress>", key_down)
fnt = ("Times New Roman", 30)
label1 = tkinter.Label(text="keycode", font=fnt)
label1.place(x=0, y=0)
label2 = tkinter.Label(text="keysysm", font=fnt)
label2.place(x=0, y=80)
root.mainloop()
