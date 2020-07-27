from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from os import listdir, getcwd, remove
from os.path import isfile, join

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Initialization -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
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

combostyle = ttk.Style()

combostyle.theme_create("combostyle", parent="alt",
                         settings = {"TCombobox":
                                     {"configure":
                                      {"selectbackground": "#396287",
                                       "fieldbackground": "#2C5F8D",
                                       "foreground": "white"
                                       }}}
                         )

combostyle.theme_use('combostyle')


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Usefull functions -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def clear():
    canvas.delete("all")
    canvas.create_image(0, 0, image = backgroundImage)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Saving cards -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def saveQuestion(event, questionEntry, answerEntry, groupCombo):
    question = questionEntry.get()
    answer = answerEntry.get()
    group = groupCombo.get()

    if question == "" and answer == "":
        messagebox.showerror("Error", "You have to fill both entry.")
    elif question == "":
        messagebox.showerror("Error", "You have to fill the 'Question' entry.")
    elif answer == "":
        messagebox.showerror("Error", "You have to fill the 'Answer' entry.")
    elif group == "":
        messagebox.showerror("Error", "Please give a name to your group.")
    elif group == "Create a new group":
        messagebox.showerror("Error", "Please choose an other group or name a new one.")
    elif "~" in group:
        messagebox.showerror("Error", "'~' : This character is not allowed")
    else:
        fileGroup = "data/" + group + ".txt"
        try:
            with open(fileGroup, "r") as file:
                data = file.readlines()

        except FileNotFoundError:
            with open(fileGroup, "w") as file:
                file.write("")

            with open(fileGroup, "r") as file:
                data = file.readlines()

        data.append(question + "\n")
        data.append(answer + "\n")

        with open(fileGroup, "w") as file:
            for i in range(len(data)):
                file.write(data[i])

        Add_Card_GUI(True)

def Add_Card_GUI(event):
    clear()

    questionLabel = canvas.create_text(200, 50, text = "Q u e s t i o n", fill = "#dbdbdb", font = myFontBig)
    questionEntry = Entry(canvas, bg = "#2C5F8D", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200,110,window = questionEntry)

    answerLabel = canvas.create_text(200, 180, text = "A n s w e r", fill = "#dbdbdb", font = myFontBig)
    answerEntry = Entry(canvas, bg = "#256A85", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200, 250, window = answerEntry)

    groupLabel = canvas.create_text(50, 330, text = "G r o u p", fill = "#dbdbdb", font = myFontLittle)

    path = getcwd() + "/data"
    groupnames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = ["Create a new group"]

    for element in groupnames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    groupCombo = ttk.Combobox(app, values = groupList, width = "27", font = myFontLittle)
    groupCombo.current(0)
    canvas.create_window(225, 330, window = groupCombo)

    SubmitButton = canvas.create_text(200, 400, text = "S u b m i t", fill = "#dbdbdb", font = myFontBig)

    def enterSubmit(event):
        canvas.itemconfig(SubmitButton, fill = "white")

    def leaveSubmit(event):
        canvas.itemconfig(SubmitButton, fill = "#dbdbdb")

    canvas.tag_bind(SubmitButton, "<Enter>", enterSubmit)
    canvas.tag_bind(SubmitButton, "<Leave>", leaveSubmit)
    canvas.tag_bind(SubmitButton, "<Button-1>", lambda event: saveQuestion(event, questionEntry, answerEntry, groupCombo))

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", Del_Add_GUI)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Deleting cards -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def Del_Card(event, questionList):
    selected = questionList.curselection()

    try:
        selectedQuestion = questionList.get(selected)
        found = False
        name = ""
        quest = ""
        for char in selectedQuestion:
            if char == "~":
                found = True
            if found == True:
                name += char
            if found == False:
                quest += char

        quest = quest[:-1]
        filename = name.replace("~ ", "").replace(" ~", "").replace("\n", "")

        path = "data/" + filename + ".txt"

        with open(path, "r") as file:
            data = file.readlines()

        index = ""

        for i in range(len(data)):
            if data[i].replace("\n", "") == quest:
                index = i
                del data[i]
                del data[i]
                break

        if index != "":
            if len(data) != 0:
                with open(path, "w") as file:
                    for element in data:
                        file.write(element)
            else:
                remove(path)

    except IndexError:
        messagebox.showerror("Error", "You have to select a question.")

    Del_Card_GUI(True)

def Del_Card_GUI(event):
    clear()

    path = getcwd() + "/data"
    groupnames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = []

    for element in groupnames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", Del_Add_GUI)

    questionList = Listbox(app, width = "40", height = "11", font = myFontLittle, bg = "#2C5F8D", fg = "white", relief = "flat", activestyle = "none")

    questionsAndGroup = []

    for i in range(len(groupList)):
        with open("data/" + groupList[i] + ".txt", "r") as file:
            data = file.readlines()
            for x in range(len(data)):
                data[x] = data[x].replace("\n", "") + " ~ " + groupList[i] + " ~"
                questionsAndGroup.append(data[x])

    pos = 0

    for i in range(len(questionsAndGroup)):
        if (i % 2) == 0:
            questionList.insert(pos, questionsAndGroup[i])
            pos += 1

    canvas.create_window(200, 180, window = questionList )

    AddLabel = canvas.create_text(200, 420, text = "D e l e t e", fill = "#dbdbdb", font = myFontBig)

    def enterAdd(event):
        canvas.itemconfig(AddLabel, fill = "white")

    def leaveAdd(event):
        canvas.itemconfig(AddLabel, fill = "#dbdbdb")

    canvas.tag_bind(AddLabel, "<Enter>", enterAdd)
    canvas.tag_bind(AddLabel, "<Leave>", leaveAdd)
    canvas.tag_bind(AddLabel, "<Button-1>", lambda event: Del_Card(event, questionList))


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Rest of the GUI -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def menu(event):
    clear()

    CardsLabel = canvas.create_text(200, 110, text = "M a n a g e   c a r d s", fill = "#dbdbdb", font = myFontBig)

    def enterAdd(event):
        canvas.itemconfig(CardsLabel, fill = "white")

    def leaveAdd(event):
        canvas.itemconfig(CardsLabel, fill = "#dbdbdb")

    canvas.tag_bind(CardsLabel, "<Enter>", enterAdd)
    canvas.tag_bind(CardsLabel, "<Leave>", leaveAdd)
    canvas.tag_bind(CardsLabel, "<Button-1>", Del_Add_GUI)

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

def Del_Add_GUI(event):
    clear()

    AddLabel = canvas.create_text(200, 110, text = "A d d   card", fill = "#dbdbdb", font = myFontBig)

    def enterAdd(event):
        canvas.itemconfig(AddLabel, fill = "white")

    def leaveAdd(event):
        canvas.itemconfig(AddLabel, fill = "#dbdbdb")

    canvas.tag_bind(AddLabel, "<Enter>", enterAdd)
    canvas.tag_bind(AddLabel, "<Leave>", leaveAdd)
    canvas.tag_bind(AddLabel, "<Button-1>", Add_Card_GUI)


    DelLabel = canvas.create_text(200, 300, text = "D e l e t e   card", fill = "#dbdbdb", font = myFontBig)

    def enterDel(event):
        canvas.itemconfig(DelLabel, fill = "white")

    def leaveDel(event):
        canvas.itemconfig(DelLabel, fill = "#dbdbdb")

    canvas.tag_bind(DelLabel, "<Enter>", enterDel)
    canvas.tag_bind(DelLabel, "<Leave>", leaveDel)
    canvas.tag_bind(DelLabel, "<Button-1>", Del_Card_GUI)

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", menu)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Start the GUI -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
clear()

menu(True)

app.mainloop()
