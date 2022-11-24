import tkinter

x, ani = 0, 0


def animation():
    global x, ani
    x += 4
    if x == 480:
        x = 0
    canvas.delete("BG")
    canvas.create_image(x - 240, 150, image=img_bg, tag="BG")
    canvas.create_image(x + 240, 150, image=img_bg, tag="BG")
    ani = (ani + 1) % 4
    canvas.create_image(240, 200, image=img_dog[ani], tag="BG")
    root.after(200, animation)


root = tkinter.Tk()
root.title("animation")
canvas = tkinter.Canvas(width=480, height=300)
canvas.pack()
img_bg = tkinter.PhotoImage(file="./images/park.png")
img_dog = [
    tkinter.PhotoImage(file="./images/dog0.png"),
    tkinter.PhotoImage(file="./images/dog1.png"),
    tkinter.PhotoImage(file="./images/dog2.png"),
    tkinter.PhotoImage(file="./images/dog3.png"),
]
animation()
root.mainloop()
