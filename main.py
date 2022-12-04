# https://www.pythontutorial.net/tkinter/

from tkinter import *
from tkinter import ttk

# Constants
G_SZ = 30
G_ROW = 8
G_COL = 10
B_SZ = 3
FONT8 = "tkDefaultFont 8"
FONT12 = "tkDefaultFont 12"
FONT16 = "tkDefaultFont 16"

# Grid types
BLANK = 0
NAME = 1
INDEX = 2
VALUE = 3
LENGTH = 4
CONTROL = 5

# Options
opt1 = [
    "Swap A and B",
    "Swap A[1] and A[3]",
    "Delete A[1]",
    "Insert X at A[1]",
    "Move A[3] before A[0]",
    "Reverse A",
]
opt2 = [
    "without tmp variable",
    "with tmp variable",
]
opt_var = [
    {"A": 3, "B": 4},
    {},
    {},
    {"X": 1},
    {},
    {},
]
opt_arr = [
    {},
    {"A": [2, 7, 1, 4, 3]},
    {"A": [1, 3, 5, 7, 9]},
    {"A": [2, 4, 6, 8]},
    {"A": [2, 7, 1, 4, 3]},
    {"A": [1, 2, 3, 5, 8]},
]

# States
task1 = 0
task2 = 0
var = opt_var[0]
arr = opt_arr[0]
grid = None
selected = None


# State change handlers
def change_task(v):
    global task1, var, arr
    task1 = opt1.index(v)
    var = opt_var[task1]
    arr = opt_arr[task1]
    if task2 == 1:
        var["tmp"] = None
    reset(None)


def change_tmp(v):
    global task2
    task2 = opt2.index(v)
    if task2 == 1:
        var["tmp"] = None
    else:
        del var["tmp"]
    reset(None)


##
# Widgets
#

# Window settings
root = Tk()
root.title("How to move variables")
app = Frame(root)
app.pack(fill=BOTH, expand=True, padx=10, pady=10)

# TOP frame
top = Frame(app)
top.pack(fill=BOTH, expand=True)
cv = Canvas(top, width=G_COL * G_SZ, height=G_ROW * G_SZ, bg="black")
cv.pack(fill=BOTH, expand=True, side=LEFT)
txt = Text(top, state="disabled", width=20, height=10, padx=5, pady=5)
txt.pack(fill=Y, side=RIGHT)

# Bottom frame
bottom = Frame(app)
bottom.pack(fill=X)
btn = ttk.Button(bottom, text="Reset")
btn.pack(side=RIGHT)
dropdown1 = ttk.OptionMenu(bottom, StringVar(app), opt1[0], *opt1, command=change_task)
dropdown1.pack(side=LEFT)
dropdown2 = ttk.OptionMenu(bottom, StringVar(app), opt2[0], *opt2, command=change_tmp)
dropdown2.pack(side=LEFT)

# Reset grid with variables and arrays
def init_grid(var, arr):
    grid = [[[BLANK, None, None]] * G_COL for _ in range(G_ROW)]
    for i, (k, v) in enumerate(var.items()):
        grid[2][i * 3 + 1] = [NAME, k, k]
        grid[2][i * 3 + 2] = [VALUE, k, v]
    for i, (k, v) in enumerate(arr.items()):
        grid[i * 2 + 4][1] = [NAME, k, k]
        for j in range(len(v)):
            grid[i * 2 + 4][j + 2] = [VALUE, f"{k}[{j}]", v[j]]
            grid[i * 2 + 5][j + 2] = [INDEX, k, j]
    if arr:
        grid[2][len(var) * 3 + 1] = [NAME, "N", "N"]
        grid[2][len(var) * 3 + 2] = [LENGTH, "N", len(list(arr.values())[0])]
        grid[2][len(var) * 3 + 3] = [CONTROL, "N", "N"]
    return grid


##
# Draw functions
#


def redraw():
    cv.delete("all")
    cv.create_text(
        (5, 5),
        anchor=NW,
        text=f"{opt1[task1]} {opt2[task2]}",
        fill="orange",
        font=FONT12,
    )
    for i in range(G_ROW):
        for j in range(G_COL):
            t, n, v = grid[i][j]
            if t == NAME:
                cv.create_text(
                    ((j + 0.5) * G_SZ, (i + 0.5) * G_SZ),
                    text=n,
                    fill="yellow",
                    font=FONT12,
                )
            elif t == INDEX:
                cv.create_text(
                    ((j + 0.5) * G_SZ, (i + 0.1) * G_SZ),
                    text=v,
                    anchor=N,
                    fill="grey",
                    font=FONT8,
                )
            elif t == VALUE or t == LENGTH:
                cv.create_rectangle(
                    (j * G_SZ, i * G_SZ),
                    ((j + 1) * G_SZ, (i + 1) * G_SZ),
                    outline="green",
                    width=2,
                )
                cv.create_text(
                    ((j + 0.5) * G_SZ, (i + 0.5) * G_SZ),
                    text=v,
                    fill="lightblue",
                    font=FONT12,
                )
            elif t == CONTROL:
                cv.create_text(
                    ((j + 0.25) * G_SZ, (i + 0.2) * G_SZ),
                    text="+",
                    fill="red",
                    font=FONT16,
                )
                cv.create_text(
                    ((j + 0.25) * G_SZ, (i + 0.9) * G_SZ),
                    text="−",
                    fill="red",
                    font=FONT16,
                )


def draw_drag(x, y, v):
    cv.create_rectangle(
        (x - G_SZ / 2, y - G_SZ / 2),
        (x + G_SZ / 2, y + G_SZ / 2),
        fill="black",
        outline="green",
        width=2,
    )
    cv.create_text((x, y), text=v, fill="yellow", font=FONT12)


def set_text(text):
    txt.config(state="normal")
    txt.delete("1.0", "end")
    txt.insert("1.0", text)
    txt.config(state="disabled")


def add_text(text):
    text = (txt.get("1.0", "end").strip() + "\n" + text).strip()
    txt.config(state="normal")
    txt.delete("1.0", "end")
    txt.insert("1.0", text)
    txt.config(state="disabled")


##
# Handlers
#


def press(e):
    global selected
    i = e.y // G_SZ
    j = e.x // G_SZ
    if 0 <= i < G_ROW and 0 <= j < G_COL:
        if grid[i][j][0] == VALUE:
            selected = (i, j)
            return
        if grid[i][j][0] == CONTROL and e.x // (G_SZ / 2) % 2 == 0:
            cnt = sum(x == VALUE for x, _, _ in grid[4])
            name = grid[4][1][1]
            if e.y // (G_SZ / 2) % 2 == 0:
                if cnt < len(grid[0]) - 2:
                    add_text(f"{grid[i][j][1]} <- {grid[i][j][1]} + 1")
                    grid[i][j - 1][2] += 1
                    grid[4][cnt + 2] = [VALUE, f"{name}[{cnt}]", None]
                    grid[5][cnt + 2] = [INDEX, name, cnt]
            else:
                if cnt > 0:
                    add_text(f"{grid[i][j][1]} <- {grid[i][j][1]} - 1")
                    grid[i][j - 1][2] -= 1
                    grid[4][cnt + 1] = [BLANK, None, None]
                    grid[5][cnt + 1] = [BLANK, None, None]
            redraw()
            return
    selected = None


def release(e):
    cv.config(cursor="arrow")
    global selected
    if selected:
        i = e.y // G_SZ
        j = e.x // G_SZ
        i2, j2 = selected
        selected = None
        if (
            not (i == i2 and j == j2)
            and 0 <= i < G_ROW
            and 0 <= j < G_COL
            and grid[i][j][0] == VALUE
        ):
            grid[i][j][2] = grid[i2][j2][2]
            add_text(f"{grid[i][j][1]} <- {grid[i2][j2][1]}\n")
            cv.config(cursor="hand2")
        redraw()


def move(e):
    i = e.y // G_SZ
    j = e.x // G_SZ
    if 0 <= i < G_ROW and 0 <= j < G_COL:
        if grid[i][j][0] == VALUE:
            cv.config(cursor="hand2")
            return
        if grid[i][j][0] == CONTROL and e.x // (G_SZ / 2) % 2 == 0:
            cv.config(cursor="hand2")
            return
    cv.config(cursor="arrow")


def drag(e):
    if selected:
        i, j = selected
        _, _, v = grid[i][j]
        redraw()
        draw_drag(e.x, e.y, v)


def reset(e):
    global grid
    set_text("")
    grid = init_grid(var, arr)
    redraw()


# # Binding
cv.bind("<ButtonPress-1>", press)
cv.bind("<ButtonRelease-1>", release)
cv.bind("<Motion>", move)
cv.bind("<B1-Motion>", drag)
btn.bind("<Button-1>", reset)

# Main
grid = init_grid(var, arr)
redraw()

app.mainloop()
