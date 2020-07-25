def CreateCard(question, answer):
    with open("data/cards.txt", "a") as file:
        file.write(question + "\n")
        file.write(answer + "\n")

question = input("Question : ")
answer = input("Answer : ")

CreateCard(question, answer)
