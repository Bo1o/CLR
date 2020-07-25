from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

app = Tk()
app.title("Create, Learn, Repeat !")
app.geometry("400x500")
app.resizable(width = False, height = False)
app.wm_attributes('-transparentcolor','green')

canvas = Canvas(app, height = 500, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.pack()

iconImage = ImageTk.PhotoImage(Image.open("data/img/logo.png"))
app.iconphoto(False, iconImage)

backgroundImage = ImageTk.PhotoImage(Image.open("data/img/background.png").resize((800, 1100)))
canvas.create_image(0, 0, image = backgroundImage)

myFont = ("Dense 50")

AddLabel = canvas.create_text(200, 110, text = "A d d  c a r d", fill = "#dbdbdb", font = myFont)

def enterAdd(event):
    canvas.itemconfig(AddLabel, fill = "white")

def leaveAdd(event):
    canvas.itemconfig(AddLabel, fill = "#dbdbdb")

canvas.tag_bind(AddLabel, "<Enter>", enterAdd)
canvas.tag_bind(AddLabel, "<Leave>", leaveAdd)


LearnLabel = canvas.create_text(200, 235, text = "L e a r n", fill = "#dbdbdb", font = myFont)

def enterLearn(event):
    canvas.itemconfig(LearnLabel, fill = "white")

def leaveLearn(event):
    canvas.itemconfig(LearnLabel, fill = "#dbdbdb")

canvas.tag_bind(LearnLabel, "<Enter>", enterLearn)
canvas.tag_bind(LearnLabel, "<Leave>", leaveLearn)


SettingsLabel = canvas.create_text(200, 360, text = "S e t t i n g s", fill = "#dbdbdb", font = myFont)

def enterSettings(event):
    canvas.itemconfig(SettingsLabel, fill = "white")

def leaveSettings(event):
    canvas.itemconfig(SettingsLabel, fill = "#dbdbdb")

canvas.tag_bind(SettingsLabel, "<Enter>", enterSettings)
canvas.tag_bind(SettingsLabel, "<Leave>", leaveSettings)




app.mainloop()
