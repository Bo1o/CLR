def DeleteCard(question):
    with open("data/cards.txt", "r") as file:
        data = file.readlines()

    toFind = question + "\n"

    for i in range(len(data)):
        if data[i] == toFind:
            del data[i]
            del data[i]
            break

    with open("data/cards.txt", "w") as file:
        for item in data:
            file.write(item)

question = input("Question : ")

DeleteCard(question)
