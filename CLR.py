from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from os import listdir, getcwd, remove
from os.path import isfile, join
from random import randint
import tkinter.font as font

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
logoandnameImage = ImageTk.PhotoImage(Image.open("data/img/logoandname_white.png").resize((64,32)))


iconImage = ImageTk.PhotoImage(Image.open("data/img/logo.png"))
app.iconphoto(False, iconImage)

myFontBig = ("Bahnschrift 40")
myFontLittle = ("Bahnschrift 13 italic")
myFontMedium = ("Bahnschrift 20")

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
    app.unbind("<Return>")
    app.unbind("<Delete>")
    app.unbind("<Escape>")
    canvas.create_image(0, 0, image = backgroundImage)
    canvas.create_image(360, 480, image = logoandnameImage)

def MakeLabel(label):
    canvas.tag_bind(label, "<Enter>", lambda event: enterLabel(event, label))
    canvas.tag_bind(label, "<Leave>", lambda event: leaveLabel(event, label))

def enterLabel(event, label):
    canvas.itemconfig(label, fill = "white")

def leaveLabel(event, label):
    canvas.itemconfig(label, fill = "#dbdbdb")


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

    questionLabel = canvas.create_text(200, 50, text = "Question", fill = "white", font = myFontBig)
    questionEntry = Entry(canvas, bg = "#2C5F8D", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200,110,window = questionEntry)

    answerLabel = canvas.create_text(200, 180, text = "Answer", fill = "white", font = myFontBig)
    answerEntry = Entry(canvas, bg = "#256A85", width = "40", font = myFontLittle, fg = "white", justify = "center", relief = "flat")
    canvas.create_window(200, 250, window = answerEntry)

    groupLabel = canvas.create_text(50, 330, text = "Group", fill = "white", font = myFontLittle)

    path = getcwd() + "/data"
    groupnames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = ["Create a new group"]

    for element in groupnames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    groupCombo = ttk.Combobox(app, values = groupList, width = "27", font = myFontLittle)
    groupCombo.current(0)
    canvas.create_window(225, 330, window = groupCombo)

    SubmitButton = canvas.create_text(200, 400, text = "Submit", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(SubmitButton)
    canvas.tag_bind(SubmitButton, "<Button-1>", lambda event: saveQuestion(event, questionEntry, answerEntry, groupCombo))

    app.bind("<Return>", lambda event: saveQuestion(event, questionEntry, answerEntry, groupCombo))

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", Del_Add_GUI)
    app.bind("<Escape>", Del_Add_GUI)


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
    except TclError:
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
    app.bind("<Escape>", Del_Add_GUI)
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

    DelCardLabel = canvas.create_text(200, 420, text = "Delete", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(DelCardLabel)
    canvas.tag_bind(DelCardLabel, "<Button-1>", lambda event: Del_Card(event, questionList))

    app.bind("<Return>", lambda event: Del_Card(event, questionList))
    app.bind("<Delete>", lambda event: Del_Card(event, questionList))


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Learning -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def Learning(event, listBox, groupList):
    groupIndex = listBox.curselection()
    try:
        group = groupList[groupIndex[0]]
        clear()

        questions = []
        answers = []

        with open("data/" + group + ".txt", "r") as file:
            lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")
            if i % 2 == 0:
                questions.append(lines[i])
            else:
                answers.append(lines[i])

        height = 100

        questionIndex = randint(0, len(questions) - 1)

        if len(questions[questionIndex]) <= 22:
            questionLabel = canvas.create_text(200, 150, text = questions[questionIndex], fill = "white", font = myFontMedium)
        else:
            chars = list(questions[questionIndex])
            for i in range (len(char) - 1):
                if chars[i] == " " and i < 22:
                    # NEEDS TO BE FILLED
                    pass

    except IndexError:
        messagebox.showerror("Error", "You have to select a group.")

def chooseLearning_Gui(event):
    clear()

    GroupLabel1 = canvas.create_text(200, 50, text = "What do you want", fill = "white", font = myFontMedium)
    GroupLabel2 = canvas.create_text(200, 100, text = "to practice ?", fill = "white", font = myFontMedium)

    groupListBox = Listbox(app, width = "40", height = "10", font = myFontLittle, bg = "#2C5F8D", fg = "white", relief = "flat", activestyle = "none")

    path = getcwd() + "/data"
    groupNames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = []

    for element in groupNames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    pos = 0

    for i in range(len(groupList)):
        groupListBox.insert(pos, groupList[i])
        pos += 1

    canvas.create_window(200, 250, window = groupListBox )

    ValidateLabel = canvas.create_text(200, 420, text = "Validate", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(ValidateLabel)

    canvas.tag_bind(ValidateLabel, "<Button-1>", lambda event: Learning(event, groupListBox, groupList))

def Learning_GUI(event):
    clear()

    path = getcwd() + "/data"
    groupnames = [f for f in listdir(path) if isfile(join(path, f))]
    groupList = []

    for element in groupnames:
        if element.endswith(".txt"):
            groupList.append(element.replace(".txt", ""))

    if len(groupList) != 0:
        chooseLearning_Gui(True)
    else:
        noCardLabel1 = canvas.create_text(200, 150, text = "Before learning,", fill = "white", font = myFontMedium)
        noCardLabel2 = canvas.create_text(200, 200, text = "you need to create cards.", fill = "white", font = myFontMedium)

        BackLabel = canvas.create_text(200, 300, text = "Back", fill = "#dbdbdb", font = myFontBig)
        MakeLabel(BackLabel)
        canvas.tag_bind(BackLabel, "<Button-1>", menu)

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", menu)
    app.bind("<Escape>", menu)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Rest of the GUI -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
def menu(event):
    clear()

    CardsLabel = canvas.create_text(200, 110, text = "Manage cards", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(CardsLabel)
    canvas.tag_bind(CardsLabel, "<Button-1>", Del_Add_GUI)

    LearnLabel = canvas.create_text(200, 235, text = "Learn", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(LearnLabel)
    canvas.tag_bind(LearnLabel, "<Button-1>", Learning_GUI)

    SettingsLabel = canvas.create_text(200, 360, text = "Settings", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(SettingsLabel)

def Del_Add_GUI(event):
    clear()

    AddLabel = canvas.create_text(200, 110, text = "Add card", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(AddLabel)
    canvas.tag_bind(AddLabel, "<Button-1>", Add_Card_GUI)

    DelLabel = canvas.create_text(200, 300, text = "Delete card", fill = "#dbdbdb", font = myFontBig)
    MakeLabel(DelLabel)
    canvas.tag_bind(DelLabel, "<Button-1>", Del_Card_GUI)

    backButton = canvas.create_image(20, 485, image = backImage)
    canvas.tag_bind(backButton, "<Button-1>", menu)
    app.bind("<Escape>", menu)


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Start the GUI -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
clear()

menu(True)

app.mainloop()
