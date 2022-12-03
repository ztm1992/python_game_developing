import tkinter
from typing import Any

import numpy as np
from pydantic import BaseModel


class Rectangle(BaseModel):
    name: str
    x: int
    y: int
    width: int
    height: int
    color: str
    canvas: Any

    class Config:
        arbitrary_types_allowed = True

    def delete(self):
        self.canvas.delete(self.name)

    def create(self):
        self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, tag=self.name
        )

    def recreate(self):
        self.delete()
        self.create()


def check_collision(rec1, rec2):
    print(np.abs(rec1.x - rec2.x), np.abs(rec1.y - rec2.y))
    collision_x = np.abs(rec1.x - rec2.x) < np.mean([rec1.width, rec2.width])
    collision_y = np.abs(rec1.y - rec2.y) < np.mean([rec1.height, rec2.height])
    if collision_x and collision_y:
        return True
    return False


def mouse_move(e, rec, base_rec):
    rec.x = int(e.x) - rec.width
    rec.y = int(e.y) - rec.height
    if check_collision(rec, base_rec):
        rec.color = "cyan"
    else:
        rec.color = "blue"
    rec.recreate()


root = tkinter.Tk()
root.title("Test collision")
canvas = tkinter.Canvas(width=600, height=400, bg="white")
canvas.pack()
rec1 = Rectangle(name="RECT1", x=50, y=50, width=120, height=60, canvas=canvas, color="blue")
rec2 = Rectangle(name="RECT2", x=300, y=100, width=120, height=160, canvas=canvas, color="red")
rec1.create()
rec2.create()
canvas.bind("<Motion>", lambda e: mouse_move(e, rec1, rec2))

root.mainloop()
