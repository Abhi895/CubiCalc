from tkinter import *
import cmath
import numpy as np

def calculate(numOne, numTwo, operation):
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
    equation = inputField.get()
    equationLabel.config(text=equation)

    inputField.delete(0, END)

    if mode == "Quadratic":
        if (equation.count("x") > 0) and equation.count("²") == 1 and equation.count("-") + equation.count("+") <= 3:
            getQuadraticAnswer(equation)
            return
    elif mode == "Cubic":
        if equation.count("x") <= 3 and equation.count("³") == 1 and equation.count("-") + equation.count("+") <= 4:
            getCubicAnswer(equation)
            return
    else:
        getNormalAnswer(equation)
        return

    inputField.insert(len(inputField.get()), "Please enter a valid equation")

def getQuadraticAnswer(quadratic):
    a,b,c = getCoefficients(quadratic, 3)
    print(a,b,c)

    discriminant = b ** 2 - 4 * a * c
    print(str(discriminant))

    if discriminant < 0:
        inputField.delete(0, "end")
        quadAnswer = "No roots"
    else:
        answerOne = ((-b + cmath.sqrt(discriminant)) / (2 * a))
        answerTwo = ((-b - cmath.sqrt(discriminant)) / (2 * a))
        quadAnswer = "x = " + str(round(answerOne.real, 3)) + ", " + str(round(answerTwo.real, 3))
        inputField.delete(0, "end")

    inputField.insert(len(inputField.get()), quadAnswer)

def getCubicAnswer(cubic):
    a, b, c, d = getCoefficients(cubic, 4)
    p = c/a - (b**2)/(3*a**2)
    q = (2*b**3)/(27*a**3) - (b*c)/(3*a**2) + d/a

    print(p, q)
    
    discriminant = round((q/2)**2, 5) + round((p/3)**3, 5)
    print(discriminant)

    additionPart = -q/2 + cmath.sqrt(discriminant)
    subtractionPart = -q/2 - cmath.sqrt(discriminant)

    if discriminant >= 0:
        answer =str(round(np.cbrt(additionPart.real)+np.cbrt(subtractionPart.real) - b/(3*a), 3))
        if discriminant == 0:
            answer += ", " + str(round(-np.cbrt(additionPart.real) - b/(3*a), 3))
    else:
        print(additionPart)
        realPart = additionPart.real
        complexPart = additionPart.imag
        r = cmath.sqrt((realPart**2 + complexPart**2)).real
        if realPart != 0:
            theta = cmath.atan(complexPart/realPart).real
            if theta < 0:
                theta = cmath.pi + theta
        else:
            theta = (cmath.pi)/2
        
        answers = [(2*(np.cbrt(r) * (cmath.cos((theta+2*x*cmath.pi)/3))).real) - b/(3*a) for x in range(3)]
        print(answers)
        answer = ", ".join([str(round(ans, 3)) for ans in sorted(answers)])

    inputField.delete(0, 'end')
    inputField.insert(len(inputField.get()), "x = " + answer)

def getCoefficients(equation, numCoefficients):
    coefficents = [0] * numCoefficients
    
    if equation[0] == "x":
        equation = "+" + equation

    for i in range(equation.count('x')):
        index = i
        cutIndex = 2

        if equation.index("x") == len(equation) - 1 or equation[equation.index("x")+1] in ["+", "-"]:
            index = numCoefficients - 2
            cutIndex = 1
       
        if equation[:2] in ["-x", "+x"]:
            coefficents[index] = int(equation[:2].replace("x", "1"))
        else:
            coefficents[index] = float("".join(x for x in equation[:equation.index("x")]))
        
        equation = equation[equation.index("x")+cutIndex:]

    if equation:
        coefficents[-1] = int(equation)
    
    return coefficents

def evaluate(equation):

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
        if ("." in finalAnswer and len(finalAnswer[finalAnswer.index("."):]) > 10):
            finalAnswer = f'{round(float(finalAnswer), 10)}'
        if "e" in finalAnswer:
            exp = int(finalAnswer[finalAnswer.index("e")+1:])
            finalAnswer = finalAnswer[:finalAnswer.index("e")] + "x10^" + str(exp)
        elif len(finalAnswer) > 15:
            floatAnswer = float(finalAnswer[0] + "." + finalAnswer[1:11])
            if len(str(floatAnswer)) >= 11:
                floatAnswer = round(floatAnswer, 9)
            finalAnswer = str(floatAnswer) + "x10^" + str(len(finalAnswer[1:]))

        inputField.insert(len(inputField.get()), finalAnswer)


def normalCalculator():
    global clear
    global mode
    global quadraticToNormal
    global opButtons

    if not quadraticToNormal:
        buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(len(buttons)):
            y = 340 - (i//3 * 100)
            x = (i%3) * 100 + 25
            createButton(x, y, buttons[i])

        clear = True
        createButton(25, 40, "C")
        clear = False

        createButton(25, 440, "0")
        createButton(125, 440, ".")
        createButton(325, 140, "-")
        createButton(325, 240, "+")
    else:
        modeSwitch.config(text="Normal")
        modeSwitch.config(command=lambda: quadraticCalculator())
        mode = "Normal"
        inputField.delete(0, END)

    xCubedButton.destroy()
    xButton.destroy()
    equationLabel.config(text="")

    btnDetails = [(325, 340, "x"), (325, 40, "+"), (125, 40, "("), (225, 40, ")"), (225, 440, "^")]

    for i in range(len(opButtons)):
        opButtons[i] = createButton(btnDetails[i][0], btnDetails[i][1], btnDetails[i][2])


def buttonPressed(text):
    inputField.insert(inputField.index(INSERT), text)

def createButton(xCoord, yCoord, text) -> Button:
    global clear

    if clear:
        btn = Button(canvas2, text=text, fg="black", bg=canvas2BG, borderwidth=0, font=("Montserrat bold", 20),
                     activebackground="#F0B75E", activeforeground="white",
                     command=lambda: inputField.delete(len(inputField.get()) - 1, END), width=3)
    else:
        btn = Button(canvas2, text=text, fg="black", bg=canvas2BG, borderwidth=0, font=("Montserrat bold", 20),
                     activebackground="#F0B75E", activeforeground="white",
                     command=lambda: buttonPressed(text), width=3)

    btn.place(x=xCoord, y=yCoord)
    return btn

def quadraticCalculator():
    global xSquaredButton
    global xButton
    global quadraticToNormal
    global opButtons

    xButton, xSquaredButton = changeMode("Quadratic", cubicCalculator, "x", "x²")

    for button in opButtons:
        button.destroy()
    quadraticToNormal = True

def cubicCalculator():
    global xButton
    global xCubedButton

    xCubedButton = changeMode("Cubic", normalCalculator, "x³")
    xButton.place(x=125, y=40)

def changeMode(newMode, nextMode, btn1, btn2=None):
    global mode

    mode = newMode
    modeSwitch.config(text=newMode)
    equationLabel.config(text="")
    modeSwitch.config(command=lambda: nextMode())
    inputField.delete(0, 'end')

    buttonOne = createButton(325, 40, btn1)
    if btn2:
        buttonTwo = createButton(225, 40, btn2)
        return buttonOne, buttonTwo
    
    return buttonOne

def allClear():
    inputField.delete(0, END)
    equationLabel.config(text="")

# MAIN PROGRAM
main = Tk()
main.title("Calculator 🔢")
main.geometry("420x720")
main.resizable(False, False)

clear = False
canvas1BG = "#68A7AD"
main["bg"] = canvas1BG

canvas2BG = "#252A34"
xSquaredButton = xButton = xCubedButton = Button()
opButtons = [Button()] * 5
quadraticToNormal = False

mode = "Normal"

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

main.mainloop()
 