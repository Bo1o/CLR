from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from PIL import ImageTk, Image
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import time

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

app = Tk()
app.title("Create, Learn, Repeat !")
app.geometry("400x500")
app.resizable(width = False, height = False)
app.wm_attributes('-transparentcolor','green')

canvas = Canvas(app, height = 500, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.pack()

backgroundImage = ImageTk.PhotoImage(Image.open("data/img/background.png").resize((800, 1100)))
backImage = ImageTk.PhotoImage(Image.open("data/img/back.png").resize((32, 32)))

iconImage = ImageTk.PhotoImage(Image.open("data/img/logo.png"))
app.iconphoto(False, iconImage)

myFontBig = ("Dense 50")
myFontLittle = ("Dense 20 italic")


def set_Background():
    canvas.create_image(0, 0, image = backgroundImage)

def clear():
    canvas.delete("all")
    set_Background()

def saveQuestion(event, questionEntry, answerEntry):
    question = questionEntry.get()
    answer = answerEntry.get()

    if question == "" and answer == "":
        messagebox.showerror("Error", "You have to fill both entry.")
        print("You need to fill both entry.")
    elif question == "":
        messagebox.showerror("Error", "You have to fill the 'Question' entry.")
        print("You need to fill the 'Question' entry.")
    elif answer == "":
        messagebox.showerror("Error", "You have to fill the 'Answer' entry.")
        print("You need to fill the 'Answer' entry.")
    else:
        pass


def menu(event):
    clear()

    CardsLabel = canvas.create_text(200, 110, text = "M a n a g e   c a r d s", fill = "#dbdbdb", font = myFontBig)

    def enterAdd(event):
        canvas.itemconfig(CardsLabel, fill = "white")

    def leaveAdd(event):
        canvas.itemconfig(CardsLabel, fill = "#dbdbdb")

    canvas.tag_bind(CardsLabel, "<Enter>", enterAdd)
    canvas.tag_bind(CardsLabel, "<Leave>", leaveAdd)
    canvas.tag_bind(CardsLabel, "<Button-1>", Add_Card_GUI)

    LearnLabel = canvas.create_text(200, 235, text = "L e a r n", fill = "#dbdbdb", font = myFontBig)

    def enterLearn(event):
        canvas.itemconfig(LearnLabel, fill = "white")

    def leaveLearn(event):
        canvas.itemconfig(LearnLabel, fill = "#dbdbdb")

    canvas.tag_bind(LearnLabel, "<Enter>", enterLearn)
    canvas.tag_bind(LearnLabel, "<Leave>", leaveLearn)

    SettingsLabel = canvas.create_text(200, 360, text = "S e t t i n g s", fill = "#dbdbdb", font = myFontBig)

    def enterSettings(event):
        canvas.itemconfig(SettingsLabel, fill = "white")

    def leaveSettings(event):
        canvas.itemconfig(SettingsLabel, fill = "#dbdbdb")

    canvas.tag_bind(SettingsLabel, "<Enter>", enterSettings)
    canvas.tag_bind(SettingsLabel, "<Leave>", leaveSettings)


def Add_Card_GUI(event):
    clear()

    questionLabel = canvas.create_text(200, 50, text = "Q u e s t i o n", fill = "#dbdbdb", font = myFontBig)
    questionEntry = Entry(canvas, bg = "#2C5F8D", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200,110,window = questionEntry)

    answerLabel = canvas.create_text(200, 220, text = "A n s w e r", fill = "#dbdbdb", font = myFontBig)
    answerEntry = Entry(canvas, bg = "#256A85", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200,290,window = answerEntry)

    SubmitButton = canvas.create_text(200, 400, text = "S u b m i t", fill = "#dbdbdb", font = myFontBig)

    def enterSubmit(event):
        canvas.itemconfig(SubmitButton, fill = "white")

    def leaveSubmit(event):
        canvas.itemconfig(SubmitButton, fill = "#dbdbdb")

    canvas.tag_bind(SubmitButton, "<Enter>", enterSubmit)
    canvas.tag_bind(SubmitButton, "<Leave>", leaveSubmit)
    canvas.tag_bind(SubmitButton, "<Button-1>", lambda event: saveQuestion(event, questionEntry, answerEntry))

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", menu)


set_Background()
menu(True)


app.mainloop()
