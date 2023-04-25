 
from tkinter import *
import pyglet
import math


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def calculate(numOne, numTwo, operation):
    answer = 0

    if operation == "+":
        answer = numOne + numTwo
    elif operation == "*":
        answer = numOne * numTwo
    elif operation == "^":
        answer = numOne ** numTwo
    elif operation == "-":
        answer = numOne - numTwo
    elif operation == "/":
        answer = numOne / numTwo

    return answer


def getAnswer():
    global equalsPressed

    equalsPressed = True
    equation = inputField.get()
    if mode == "Quadratic":
        if (equation.count("x") <= 2) and equation.count("²") == 1 and equation.count("-") + equation.count("+") <= 3:
            equationLabel.config(text=equation)
            getQuadraticAnswer(equation)
        else:
            inputField.delete(0, "end")
            inputField.insert(len(inputField.get()), "Please enter a valid quadratic")
    elif mode == "Cubic":
        if equation.count("x") <= 3 and equation.count("²") == 1 and equation.count("³") == 1 and equation.count("-") + equation.count:
            print()
    else:
        getNormalAnswer(equation)


def getQuadraticAnswer(quadratic):
    a = 1
    b = 0
    c = 0

    if quadratic[0] != "x":
        if quadratic[0] == "-":
            a = int("".join(x for x in quadratic[1:quadratic.index("x")])) * -1
        else:
            a = int("".join(x for x in quadratic[:quadratic.index("x")]))

    if quadratic.count('x') > 1:
        if quadratic[quadratic.index("²") + 2] != "x":
            b = int("".join([x for x in quadratic[quadratic.index("²") + 2:quadratic.replace("x", "", 1).find('x')+1]]))
            if quadratic[quadratic.index("²") + 1] == "-":
                b *= -1
        else:
            b = 1

    if quadratic[-1] != "x":
        c = int("".join([quadratic[::-1][x] for x in range(quadratic[::-1].index("x") - 1)][::-1]))
        if quadratic[::-1][quadratic[::-1].index("x") - 1] == "-":
            c *= -1

    discriminant = b ** 2 - 4 * a * c
    print(str(discriminant))

    if discriminant < 0:
        inputField.delete(0, "end")
        quadAnswer = "No roots"
    else:
        answerOne = ((-b + math.sqrt(discriminant)) / (2 * a))
        answerTwo = ((-b - math.sqrt(discriminant)) / (2 * a))
        quadAnswer = "x = " + str(round(answerOne, 3)) + ", " + str(round(answerTwo, 3))
        inputField.delete(0, "end")

    inputField.insert(len(inputField.get()), quadAnswer)

def getIndex(value, arrayOne, arrayTwo):
    return arrayOne.index((value, [y[1] for y in arrayOne if y[0] == arrayTwo[0]][0]))


def evaluate(equation):

    equationLabel.config(text=inputField.get())
    equation = equation.replace("÷", "/")
    equation = equation.replace("x", "*")

    possibleOps = "^*/+-"

    if equation != "" :
        print(equation)
        operations = [equation[x] for x in range(1, len(equation)) if equation[x] in possibleOps and equation[x-1] not in possibleOps]
        indexes = [x for x in range(1, len(equation)) if equation[x] in possibleOps and equation[x-1] not in possibleOps]
        indexes.insert(0, -1)

        numbers = [float(equation[indexes[x-1]+1:indexes[x]]) for x in range(1, len(indexes))]
        numbers.append(float(equation[indexes[-1]+1:]))

        print(equation)

        while len(numbers) > 1:
            presentOps = [x for x in possibleOps if x in operations]
            if presentOps[0] == "^":
                indexOfOperation = operations.index("^")
            elif presentOps[0] == "*" or presentOps[0] == "/":
                if "*/".replace(presentOps[0], "") in presentOps:
                    indexOfOperation = min([operations.index('/'), operations.index('*')])
                else:
                    indexOfOperation = operations.index(presentOps[0])
            else:
                if "+-".replace(presentOps[0], "") in presentOps:
                    indexOfOperation = min([operations.index('+'), operations.index('-')])
                else:
                    indexOfOperation = operations.index(presentOps[0])


            print(numbers)
            print(operations)
            
            answer = calculate(numbers[indexOfOperation], numbers[indexOfOperation+1], operations[indexOfOperation][0])
            numbers.pop(indexOfOperation)
            numbers[indexOfOperation] = answer
            operations.pop(indexOfOperation)

        finalAnswer = str(numbers[0])
        
        if float(finalAnswer).is_integer():
            finalAnswer = str(int(float(finalAnswer)))

        return finalAnswer
    
def getNormalAnswer(equation):

    if "(" in equation and equation.count("(") == equation.count(")"):
        while "(" in equation:
            openIndex = len(equation) - equation[::-1].index("(") - 1
            closedIndex = [x for x in equation[openIndex:]].index(')') + openIndex
            tempAnswer = evaluate(equation[openIndex+1:closedIndex])
            equation = equation[:openIndex] + tempAnswer + equation[closedIndex+1:]

    elif "(" not in equation:
        print(equation)
        evaluate(equation)
    else:
        inputField.delete(0, "end")
        inputField.insert(len(inputField.get()), "Equation Not Valid")


    print("e-" + equation)

    finalAnswer = evaluate(equation)
    inputField.delete(0, "end")
    
    if finalAnswer:
        if "." in finalAnswer:
            if len(finalAnswer[finalAnswer.index("."):]) > 10:
                finalAnswer = f'{round(float(finalAnswer), 10)}'


        inputField.insert(len(inputField.get()), finalAnswer)


def normalCalculator():
    global clear
    global equals
    global numbers
    global openBracketBtn
    global closeBracketBtn
    global powerBtn
    global divideBtn
    global multiplyBtn
    global mode
    global xCubedButton

    if not quadraticToNormal:
        clear = True
        createButton(25, 40, "C")
        clear = False
        numbers = True
        createButton(25, 140, "7")
        createButton(125, 140, "8")
        createButton(225, 140, "9")
        createButton(25, 240, "4")
        createButton(125, 240, "5")
        createButton(225, 240, "6")
        createButton(25, 340, "1")
        createButton(125, 340, "2")
        createButton(225, 340, "3")
        numbers = False
        createButton(25, 440, "0")
        createButton(125, 440, ".")
        createButton(325, 140, "-")
        createButton(325, 240, "+")
    else:
        modeSwitch.config(text="Normal")
        modeSwitch.config(command=lambda: quadraticCalculator())
        mode = "Normal"
        inputField.delete(0, END)

    multiplyBtn = createButton(325, 340, "x")
    divideBtn = createButton(325, 40, "÷")
    openBracketBtn = createButton(125, 40, "(")
    closeBracketBtn = createButton(225, 40, ")")
    powerBtn = createButton(225, 440, "^")
    xCubedButton.destroy()
    xButton.destroy()
    equationLabel.config(text="")


def numberPressed(text):
    global equalsPressed
    if equalsPressed:
        inputField.delete(0, 'end')
        equalsPressed = False
    inputField.insert(len(inputField.get()), text)


def characterPressed(text):
    global equalsPressed
    if equalsPressed:
        equalsPressed = False
    inputField.insert(len(inputField.get()), text)


def createButton(xCoord, yCoord, text) -> Button:
    global clear
    global numbers

    if clear:
        btn = Button(canvas2, text=text, fg="black", bg=canvas2BG, borderwidth=0, font=("Montserrat bold", 20),
                     activebackground="#F0B75E", activeforeground="white",
                     command=lambda: inputField.delete(len(inputField.get()) - 1, END), width=3)
    elif numbers:
        btn = Button(canvas2, text=text, fg="black", bg=canvas2BG, borderwidth=0, font=("Montserrat bold", 20),
                     activebackground="#F0B75E", activeforeground="white",
                     command=lambda: numberPressed(text), width=3)
    else:
        btn = Button(canvas2, text=text, fg="black", bg=canvas2BG, borderwidth=0, font=("Montserrat bold", 20),
                     activebackground="#F0B75E", activeforeground="white",
                     command=lambda: characterPressed(text), width=3)

    btn.place(x=xCoord, y=yCoord)
    return btn


def quadraticCalculator():
    global xSquaredButton
    global xButton
    global mode
    global quadraticToNormal

    mode = "Quadratic"
    modeSwitch.config(text="Quadratic")
    equationLabel.config(text="")
    # modeSwitch.config(command=lambda: cubicCalculator())
    modeSwitch.config(command=lambda: normalCalculator())
    inputField.delete(0, 'end')
    openBracketBtn.destroy()
    xSquaredButton = createButton(125, 40, text="x²")
    closeBracketBtn.destroy()
    xButton = createButton(225, 40, text="x")
    multiplyBtn.destroy()
    divideBtn.destroy()
    powerBtn.destroy()
    quadraticToNormal = True

def cubicCalculator():
    global xSquaredButton
    global xButton
    global xCubedButton
    global mode

    modeSwitch.config(text="Cubic")
    equationLabel.config(text="")
    modeSwitch.config(command=lambda: normalCalculator())
    inputField.delete(0, 'end')
    xSquaredButton.place(x=225, y=40)
    xButton.place(x=325, y=40)
    xCubedButton = createButton(125, 40, text="x³")
    mode = "Cubic"

def allClear():
    inputField.delete(0, END)
    equationLabel.config(text="")


# MAIN PROGRAM
main = Tk()
main.title("Calculator 🔢")
main.geometry("420x720")
main.resizable(False, False)

numbers = False
clear = False
equals = False
equalsPressed = False
canvas1BG = "#68A7AD"
main["bg"] = canvas1BG

canvas2BG = "#252A34"
openBracketBtn = Button()
closeBracketBtn = Button()
multiplyBtn = Button()
powerBtn = Button()
divideBtn = Button()
xSquaredButton = Button()
xButton = Button()
xCubedButton = Button()
quadraticToNormal = False
quadAnswer = ""

answer = ""
equationArray = []
equationArrayTwo = []
mode = "Normal"
cubicMode = False

# pyglet.font.add_file('Montserrat-VariableFont_wght.ttf')

canvas = Canvas(main, width="400", height="190", highlightthickness=0,
                highlightcolor=canvas1BG)
canvas.create_rectangle(480, 200, 0, 0, outline=canvas1BG, fill=canvas1BG)
canvas.pack()

equationLabel = Label(canvas, text="", font=("Arial", 20), anchor="e", width=21, bg=canvas1BG, fg="black")
equationLabel.place(x=150, y=50)

inputField = Entry(canvas, bg=canvas1BG, highlightthickness=0, font=('Arial bold', 35), borderwidth=0, fg="white",
                   justify="right")
inputField.pack(pady=(100, 15), padx=(5, 5))

clrButton = Button(canvas, text="AC", borderwidth=0, bg=canvas2BG, command=lambda: allClear(),
                   fg="black", width=4, height=2)
clrButton.place(x=20, y=50)

modeSwitch = Button(canvas, text="Normal", bd=0, fg="black", font='Montserrat 12', bg=canvas1BG,
                         command=lambda: quadraticCalculator())
modeSwitch.place(x=160, y=10)

canvas2 = Canvas(main, width="425", height="600", bg=canvas2BG, highlightthickness=10, highlightbackground=canvas2BG,
                 highlightcolor=canvas2BG)
canvas2.pack_propagate(False)
canvas2.pack()

normalCalculator()
equalsButton = Button(canvas2, text="=", fg="black", activebackground=canvas2BG, borderwidth=0, font=("Montserrat", 20),
                      width=3, activeforeground="white",
                      command=lambda: getAnswer(), bg="#F0B75E")
equalsButton.place(x=325, y=440)

main.bind("<Return>", getAnswer())

main.mainloop()
 