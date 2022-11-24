import tkinter as tk

import numpy as np
from scipy import sparse as sps


def generate_block(n_row, n_col, bound=1):
    block = np.zeros(n_row, n_col)
    block[1 : n_row - 1, 1 : n_col - 1] = 1
    return block


def rotate_block(block, theta=np.pi / 4):
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
    rows = []
    for row in rotated_mat:
        nonzero_cols = row.nonzero()[1]
        if len(nonzero_cols):
            row[:, min(nonzero_cols) : max(nonzero_cols) + 1] = 1
            rows.append(row)

    return sps.vstack(rows).todense()


def generate_map(n_row, n_col, mask_size=0.3):
    mask_row = 2


root = tk.Tk()
root.title("Map")
n_row = 10
n_col = 14
canvas = tk.Canvas(width=24 * n_col, height=24 * n_row)
canvas.pack()
img = []
for i in range(4):
    img.append(tk.PhotoImage(file=f"images/chip{i}.png"))
map_data = generate_map(n_row, n_col)
