import tkinter as tk

import numpy as np
from scipy import sparse as sps


def generate_block(n_row, n_col, mask_n_row, mask_n_col):
    block = np.zeros((n_row, n_col))
    row_start = np.random.randint(0, n_row - mask_n_row)
    col_start = np.random.randint(0, n_col - mask_n_col)
    block[row_start : row_start + mask_n_row, col_start : col_start + mask_n_col] = 1
    return block


def rotate_block(block, theta):
    h, w = block.shape
    S = np.array([[np.sin(theta), np.cos(theta), 0], [-np.cos(theta), np.sin(theta), 0], [0, 0, 1]])
    L = np.array([[1, 0, 0], [0, -1, 0], [-0.5 * w, 0.5 * h, 1]])
    R = np.array([[1, 0, 0], [0, -1, 0], [0.5 * w, 0.5 * h, 1]])
    row = []
    col = []
    val = []
    for i in range(h):
        for j in range(w):
            i_prime, j_prime, _ = np.array([i, j, 1]).dot(L).dot(S).dot(R)
            row.append(max(min(int(i_prime), h - 1), 0))
            col.append(max(min(int(j_prime), w - 1), 0))
            val.append(block[i, j])
    rotated_mat = sps.csr_matrix((val, (row, col)), shape=(h, w))
    return consistant_block(rotated_mat)


def consistant_block(block):
    rows = []
    for row in block:
        nonzero_cols = row.nonzero()[1]
        if len(nonzero_cols):
            row[:, min(nonzero_cols) : max(nonzero_cols) + 1] = 1
            rows.append(row)
    return sps.vstack(rows)


def generate_map(n_row, n_col, mask_size=0.3):
    mask_n_row = int(n_row * mask_size)
    mask_n_col = int(n_col * mask_size)
    block = generate_block(n_row, n_col, mask_n_row, mask_n_col)
    theta = 2 * np.pi / np.random.randint(1, 10)
    block = rotate_block(block, theta=theta)
    mask_pos = block.nonzero()
    map_data = np.random.randint(0, 3, (n_row, n_col))
    map_data[mask_pos] = 3
    return map_data


def mouse_click(e, map_data):
    print(f"position of the momuse: ({e.x}, {e.y})")
    px, py = int(e.x / 48), int(e.y / 48)
    if px in range(map_data.shape[1]) and py in range(map_data.shape[0]):
        data = map_data[py, px]
        print(f"the map type is {CHIP_NAME[data]}")


root = tk.Tk()
root.title("Map")
n_row = 14
n_col = 14
canvas = tk.Canvas(width=48 * n_col, height=48 * n_row)
canvas.pack()
CHIP_NAME = ["grass", "flower", "tree", "water"]
img = []
for i in range(4):
    img.append(tk.PhotoImage(file=f"./images/chip{i}.png"))
map_data = generate_map(n_row, n_col, 0.5)
for i in range(n_row):
    for j in range(n_col):
        canvas.create_image(j * 48 + 24, i * 48 + 24, image=img[map_data[i, j]])
canvas.bind("<Button>", lambda e: mouse_click(e, map_data=map_data))
root.mainloop()
