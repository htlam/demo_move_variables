# https://www.pythontutorial.net/tkinter/

from tkinter import *

# Constants
G_SZ = 30
G_ROW = 10
G_COL = 15
B_SZ = 3
FONT = "tkDefaultFont 12"
FONT2 = "tkDefaultFont 8"

# Grid types
BLANK = 0
NAME = 1
INDEX = 2
VALUE = 3

# States
var = {}
arr = {}
grid = None
selected = None

##
# Widgets
#

# Window settings
root = Tk()
root.title("How to move variables")

# Frame for padding
app = Frame(root)
app.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Canvas
cv = Canvas(app, width=G_COL * G_SZ, height=G_ROW * G_SZ, bg="black")
cv.pack(fill=BOTH, expand=True)

# Textbox
txt = Text(app, height=10, padx=5, pady=5)
txt["state"] = "disabled"
txt.pack(fill=X)

# Bottom frame
bottom = Frame(app)
btn = Button(bottom, text="Reset")
btn.pack()
bottom.pack()

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
    return grid


# Redraw canvas
def redraw():
    cv.delete("all")
    cv.create_text((5, 5), anchor=NW, text=task, fill="orange", font=FONT)
    for i in range(G_ROW):
        for j in range(G_COL):
            t, n, v = grid[i][j]
            if t == NAME:
                cv.create_text(
                    ((j + 0.5) * G_SZ, (i + 0.5) * G_SZ),
                    text=n,
                    fill="yellow",
                    font=FONT,
                )
            elif t == INDEX:
                cv.create_text(
                    ((j + 0.5) * G_SZ, (i + 0.1) * G_SZ),
                    text=v,
                    anchor=N,
                    fill="grey",
                    font=FONT2,
                )
            elif t == VALUE:
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
                    font=FONT,
                )


# Draw draging value
def draw_drag(x, y, v):
    cv.create_rectangle(
        (x - G_SZ / 2, y - G_SZ / 2),
        (x + G_SZ / 2, y + G_SZ / 2),
        fill="black",
        outline="green",
        width=2,
    )
    cv.create_text((x, y), text=v, fill="yellow", font=FONT)


##
# Handlers
##


def press(e):
    global selected
    i = e.y // G_SZ
    j = e.x // G_SZ
    if 0 <= i < G_ROW and 0 <= j < G_COL and grid[i][j][0] == VALUE:
        selected = (i, j)
    else:
        selected = None


def release(e):
    cv.config(cursor="arrow")
    global selected
    if selected:
        i = e.y // G_SZ
        j = e.x // G_SZ
        i2, j2 = selected
        selected = None
        if 0 <= i < G_ROW and 0 <= j < G_COL and grid[i][j][0] == VALUE:
            _, n, v = grid[i][j]
            grid[i][j][2] = grid[i2][j2][2]
            print(f"{grid[i][j][1]} <- {grid[i2][j2][1]}")
            cv.config(cursor="hand2")
        redraw()


def move(e):
    i = e.y // G_SZ
    j = e.x // G_SZ
    if 0 <= i < G_ROW and 0 <= j < G_COL and grid[i][j][0] == VALUE:
        cv.config(cursor="hand2")
    else:
        cv.config(cursor="arrow")


def drag(e):
    if selected:
        i, j = selected
        _, _, v = grid[i][j]
        redraw()
        draw_drag(e.x, e.y, v)


def reset(e):
    global grid
    grid = init_grid(var, arr)
    redraw()


# # Binding
cv.bind("<ButtonPress-1>", press)
cv.bind("<ButtonRelease-1>", release)
cv.bind("<Motion>", move)
cv.bind("<B1-Motion>", drag)
btn.bind("<Button-1>", reset)

# Main
task = "Swap a and b"
var = {"X": 3, "Y": 4}
arr = {
    "A": [1, 3, 5],
    "B": [2, 4, 6, 8],
}
grid = init_grid(var, arr)
redraw()

# Add code
txt["state"] = "normal"
txt.insert("1.0", "Demo")
txt["state"] = "disabled"

app.mainloop()
