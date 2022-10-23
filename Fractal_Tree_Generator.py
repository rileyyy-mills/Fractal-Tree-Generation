import os
from re import X
import sys
import math
from tracemalloc import start
import graphics


def main():

    D = 10     # Distance/how long each branch is

    print("This program will randomly generate a drawing of a plant based on your input!")

    ##generationCount = int(input("\nHow many generations would you like for your plant? "))

    ##stemAngle = float(input("\nWhat is the angle you would like to have between the plant stems? "))

    ##file = str(input("\nFile with generation grammar: "))

    generations = 6        ##TEMP
    stemAngle = 25        ##TEMP
    file = "grammar.txt"    ##TEMP

    # opens file and returns grammaR
    grammar = getGrammarRules(os.path.join(sys.path[0],file))
    grammar = setupGrammar(grammar)

    window, startPoint = setupWindow(D)
    
    startAngle = (stemAngle + 90) * (math.pi / 180.0)
    startState = (startPoint, startAngle)

    # generates plant drawing within window
    window = generatePlant(window, generations, D, stemAngle, grammar, startState)


def getGrammarRules(fileName):
    # takes the filename inputted and opens it for grammar; determines start symbol(s) and returns a list of three items

    grammarFile = open(fileName)
    grammarList = []    # A list of all the necessary grammar information; this is what gets returned at end of funct
    axiom = ""   # Contains the axiom for the generated image(s)
    rules = {}

    for line in grammarFile:
        # iterates over each line in the grammarFile & formats line for reading

        line = line.strip('\n')
        line = line.strip()
        line = line.split('=')
        
        if len(line) == 1:
            # Inserts axiom as first item in list
            axiom = str(line[0])
            grammarList.append(axiom)
            
        elif len(line) == 2:
            # Inserts rule definitions into dictionary
            rules[line[0]] = line[1]

    grammarList.append(rules)
    return grammarList


def setupGrammar(grammarList):
    axiom  = grammarList[0]
    rules = grammarList[1] 
    newAxiom = ""


    for i in range(len(axiom)):
        letter = axiom[i]

        if (letter in rules):
            #print("YES!",letter,"=",rules[letter])
            newAxiom += rules[letter]
        else:
            newAxiom += letter

    grammarList[0] = newAxiom

    return grammarList
      

def setupWindow(D):
    # gets a title and window size and returns a window that can be modified

    import graphics


    windowTitle = 'Plant Generation'

    #determines window size based on how many generations the user wants
    if D < 7:
        windowSize = 200
    elif D >= 7 and D < 9:
        windowSize = 400
    else:
        windowSize = 600

    windowSize = 600

    window = graphics.GraphWin(windowTitle, windowSize, windowSize)

    startPoint = graphics.Point((windowSize//4), windowSize)

    return (window, startPoint)


def generatePlant(window, generationCount, F, A, grammarList, startState):

    # window = displays plant image;
    # generationCount == number of generations left to draw; counts down to 0;   
    # F == length of each line drawn;   
    # A == angle of each line drawn;
    # grammarList == a list containg all necessary grammar information;

    if (generationCount == 0):    
        window.getMouse()
        return

    else: 

        # axiom = symbol instructions
        # currentState = tuple containing [(startPoint), sumRadianAngle]
        # sumRadianAngle = angle that lines will be drawn
        # stateStack[] = used to access previous states pushed onto stack

        axiom = grammarList[0]    
        currentState = startState
        startAngle = currentState[1]
        stateStack = []   

        # Axiom is iterated through & each letter's corresponding instruction gets executed
        for i in range(len(axiom)):

            letter = axiom[i]
            #print("index =",i,"  letter: ",letter)
         
            # Pushes currentState onto stateStack
            if (letter == '['):
                stateStack.append((currentState))
                
            # Pops stateStack and updates currentState with new values
            elif (letter == ']'):
                currentState = stateStack[-1]
                #startPoint = currentState[0]
                #sumRadianAngle = currentState[1]
                stateStack.remove(stateStack[-1])
                #print("STATESTACK POPPED:",stateStack,"\nCURRENT STATE:",currentState,"\n")
                
            # Executes corresponding instruction & returns new currentState with updated values
            elif ((letter == '+') or (letter == '-') or (letter == 'F')):
                currentState = executeLetter(window, F, A, letter, currentState)

        grammarList = setupGrammar(grammarList)
        currentState = (currentState[0], startAngle)
        generatePlant(window, (generationCount-1), (F*0.7), A, grammarList, startState)


def executeLetter(window, F, A, letter, originState):

    # Starting coordinate & angle values are extracted from originState
    startPoint = originState[0]
    sumRadianAngle = originState[1]

    x1 = startPoint.getX()
    y1 = startPoint.getY()

    DEGREES_TO_RADIANS = (math.pi / 180.0)

    if (letter == '-'):
        sumRadianAngle = sumRadianAngle + (DEGREES_TO_RADIANS * A)

    if  (letter == '+'):
        sumRadianAngle = sumRadianAngle - (DEGREES_TO_RADIANS * A)

    if (letter == 'F'):
        x2 = x1 - (math.cos(sumRadianAngle) * F)
        y2 = y1 + (math.sin(sumRadianAngle) * (-1 * F))  
        startPoint = graphics.Point(x1, y1)    
        newPoint = graphics.Point(x2, y2)
        plantLine = graphics.Line(startPoint, newPoint)
        plantLine.draw(window)
        x1 = x2
        y1 = y2

    startPoint = graphics.Point(x1,y1)
    currentState = (startPoint, sumRadianAngle)

    return currentState


main()