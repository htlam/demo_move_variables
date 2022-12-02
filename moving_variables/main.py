# https://www.pythontutorial.net/tkinter/

from tkinter import *

# Window settings
root = Tk()
root.title("How to move variables")

# Frame for padding
app = Frame(root)
app.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Canvas
cv = Canvas(app, width=500, height=200, bg="black")
cv.pack(fill=BOTH, anchor=CENTER, expand=True)


def draw(text):
    cv.create_text(
        (55, 20),
        text=text,
        fill="orange",
        font="tkDefaultFont 16",
    )


draw("Swapping")


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

app.mainloop()
