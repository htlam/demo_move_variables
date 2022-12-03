# https://www.pythontutorial.net/tkinter/

from tkinter import *

# Constants
G_SZ = 30
G_ROW = 10
G_COL = 15
B_SZ = 3
FONT = "tkDefaultFont 12"
FONT2 = "tkDefaultFont 8"

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

# Add code
txt["state"] = "normal"
txt.insert("1.0", "Demo")
txt["state"] = "disabled"

# States
task = ""
pos = None
val = 0
var = {}
arr = {}

##
# Handlers
##


def get_var(pos):
    return "X"


def get_val(pos):
    return 1


def draw_box(x, y, val, fg="green", bg="black", tc="yellow", font=FONT):
    cv.create_rectangle((x, y), (x + G_SZ, y + G_SZ), fill=bg)
    cv.create_line((x, y), (x + G_SZ, y), width=B_SZ, fill=fg)
    cv.create_line((x, y), (x, y + G_SZ), width=B_SZ, fill=fg)
    cv.create_line((x, y + G_SZ), (x + G_SZ, y + G_SZ), width=B_SZ, fill=fg)
    cv.create_line((x + G_SZ, y), (x + G_SZ, y + G_SZ), width=B_SZ, fill=fg)
    cv.create_text((x + G_SZ / 2, y + G_SZ / 2), text=val, fill=tc, font=font)


def draw_text(x, y, txt, fill="yellow", font=FONT, anchor=CENTER):
    cv.create_text((x, y), text=txt, fill=fill, font=font, anchor=anchor)
    pass


def draw_var(pos, name, val):
    x, y = pos
    draw_text((x - 0.5) * G_SZ, (y + 0.5) * G_SZ, name)
    draw_box(x * G_SZ, y * G_SZ, val, fg="green", bg="black", tc="lightblue")


def draw_arr(pos, name, arr):
    x, y = pos
    draw_text((x - 0.5) * G_SZ, (y + 0.5) * G_SZ, name)
    for i in range(len(arr)):
        draw_text(
            (x + i + 0.5) * G_SZ,
            (y - 0.1) * G_SZ,
            i,
            anchor=S,
            fill="grey",
            font=FONT2,
        )
        draw_box(
            (x + i) * G_SZ, y * G_SZ, arr[i], fg="green", bg="black", tc="lightblue"
        )


def draw_mv(x, y, val):
    draw_box(x, y, val, fg="green", bg="black", tc="yellow")


def redraw():
    cv.delete("all")
    cv.create_text((5, 5), anchor=NW, text=task, fill="orange", font=FONT)
    draw_var((2, 2), "x", 3)
    draw_arr((2, 4), "A", [1, 3, 5])


##
# Handlers
##


def press(e):
    cv.config(cursor="hand2")
    global pos, val
    pos = (e.x // G_SZ, e.y // G_SZ)
    val = get_val(pos)
    move(e)


def release(e):
    cv.config(cursor="arrow")
    global pos
    pos = None


def move(e):
    if pos:
        redraw()
        draw_mv(e.x - G_SZ / 2, e.y - G_SZ / 2, 10)


def reset(e):
    redraw("")


# Binding
cv.bind("<ButtonPress-1>", press)
cv.bind("<ButtonRelease-1>", release)
cv.bind("<B1-Motion>", move)
btn.bind("<Button-1>", reset)

# Main
task = "Swap a and b"
redraw()

app.mainloop()
