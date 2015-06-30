#Author: Kyle Reinholt
#Date: 6/25/15
#Program: Json Filter
#Purpose: To extract execution points from the json trace produced from InMemory.java that are intended for visualization

import sys

with open('jsontrace.txt','r') as f:
    read_data = f.read()

f.closed

splitter = '"' + "trace" + '"' + ':'

userCode, wholeTrace = read_data.split(splitter)

class Event(object):
    
    def __init__(self):
        self.trace = ""
        self.lineNumber = 0

    def set_Event(self, trace):
        self.trace = trace

    def set_Line(self, lineNumber):
        self.lineNumber = lineNumber
    
    def get_Event():
        return self.trace

    def get_Line():
        return self.lineNumber

    
class EventManager(object):
    
    def __init__(self):
        self.listOfEvents = []
        self.filteredEvents = []

    def get_Line_Number(self, index):
        if is_empty(self.listOfEvents) == True:
            print("list is empty")
        else:
            tempEvent = self.listOfEvents[index]
            return tempEvent.lineNumber

    def set_Event(self, index, event):
        self.filteredEvents[index] = event
    
    def get_Event(index):
        return self.filteredEvents[index]

    def add_Event(self, event):
        self.listOfEvents.append(event)

    def trace_List(self):
        myList = []
        for x in range(0,len(self.filteredEvents)):
            temp = Event()
            temp = self.filteredEvents[x]
            myList.append(temp.trace)

        return myList

    def print_Events(self):
        if (len(self.filteredEvents) == 0):
            print("List of events is empty")
        else:
            for x in range(0, len(self.filteredEvents)):
                tempEvent = self.filteredEvents[x]
                print(tempEvent.trace)

    def verify_Events(self):
        currentLine = 0
        nextLine = 0
        eventCounter = 0
        counter = 1
        
        originalLineNum = self.get_Line_Number(0)
        currentLine = originalLineNum

        length = len(self.listOfEvents) - 1
    
        while counter < length+1:
            nextLine = self.get_Line_Number(counter)

            if (currentLine+1 == nextLine and nextLine > originalLineNum) or (currentLine+2 == nextLine and nextLine > originalLineNum) or (currentLine+3 == nextLine and nextLine > originalLineNum) or (currentLine+4 == nextLine and nextLine > originalLineNum) or (currentLine+5 == nextLine and nextLine > originalLineNum):
                self.filteredEvents.append(self.listOfEvents[eventCounter])
                eventCounter = eventCounter + 1
                currentLine = nextLine
                counter = counter + 1
            else:
                currentLine = nextLine
                eventCounter = eventCounter + 1
                counter = counter + 1

        
        self.filteredEvents.append(self.listOfEvents[length])

    def modify_Lines(self, code):
        lineNumber = 0
        eventNumber = 0

        while lineNumber != len(code):
            modify = Event()
            tempString = ""
            tempLine = 0

            modify = self.filteredEvents[eventNumber]
            tempString = modify.trace
            tempLine = modify.lineNumber

            if(code[lineNumber] == "newline"):
                lineNumber = lineNumber + 1
            else:
                originalLine = str(tempLine)
                newLine = str(lineNumber+1)
                tempString = tempString.replace(originalLine,newLine)
                modifiedEvent = Event()
                modifiedEvent.set_Event(tempString)
                modifiedEvent.set_Line(lineNumber+1)
                self.filteredEvents[eventNumber] = modifiedEvent

                eventNumber = eventNumber + 1
                lineNumber = lineNumber + 1

        lastEvent = Event()
        lastEvent = self.filteredEvents[eventNumber]
        tempLine = lastEvent.lineNumber
        tempString = lastEvent.trace

        oldLine = str(tempLine)

        secondTLEvent = Event()
        secondTLEvent = self.filteredEvents[eventNumber-1]
        otherLine = secondTLEvent.lineNumber

        newLine = str(otherLine)

        tempString = tempString.replace(oldLine,newLine)
        
        modifiedEvent = Event()
        modifiedEvent.set_Event(tempString)
        modifiedEvent.set_Line(otherLine)
        self.filteredEvents[eventNumber] = modifiedEvent        
                
                
    
class TraceAnalyzer(object):

    def __init__(self): 
        self.eventManager = EventManager()

    def handleEverything(self, userCode, inTrace):
        filterPoints = self.exe_Point_Finder
        filterPoints(inTrace)
        
        filteredEvents = self.eventManager.verify_Events
        filteredEvents()
        modifyLines = self.eventManager.modify_Lines(userCode) 

        events = []
        events = self.eventManager.trace_List()

        orig_stdout = sys.stdout
        f = file('filteredJSON.js', 'w')
        sys.stdout = f

        first = "var testvisualizerTrace = {\"code\":\""

        code = ""
        
        for x in range (0,len(userCode)):
            if userCode[x] == "newline":
                code = code + "\\n" + " "
            else:
                code = code + userCode[x] + "\\n"
        second = "\",\"trace\":["

        trace = ""
        for y in range(0,len(events)):
            if y == len(events)-1:
                tempString = events[y]
                tempString = tempString[:-1]
                trace = trace + tempString
                trace = trace + "],\"userlog\":\"Debugger VM maxMemory: 807M \\n \"}"
                trace = trace + "\n" + "$(document).ready(function() { \n \n \t var testvisualizer = new ExecutionVisualizer('testvisualizerDiv', testvisualizerTrace,{embeddedMode: false, lang: 'java', heightChangeCallback: redrawAllVisualizerArrows}); \n \n \tfunction redrawAllVisualizerArrows() { \n \n \t \t if (testvisualizer) testvisualizer.redrawConnectors(); \n \t } \n \n $(window).resize(redrawAllVisualizerArrows); \n});"
            else: 
                tempString = events[y]
                trace = trace + tempString + "\n"
                
        printToFile = first + code + second + trace

        print printToFile
        
        sys.stdout = orig_stdout
        f.close()
        
    def is_empty(self, any_structure):
        if any_structure:
            return False
        else:
            return True    

    def extract_Line_Num(self, string):

        line = string.replace('"'," ")
        line = line.replace('{'," ")
        line = line.replace(':'," ")
        line = line.replace(','," ")
        line = line.replace('['," ")
        line = line.replace('('," ")
        line = line.replace(']'," ")
        line = line.replace('}'," ")
        line = line.replace(')'," ")
        
        line = [int(s) for s in line.split() if s.isdigit()]
        
        return line[0]

    def verify_Exe_Point(self, on, off, inPoint):
        
        addExePoint = False
        exeTrace = Event()

        if on == True and off == False:
            exeTrace.set_Event(inPoint)
            exeTrace.set_Line(self.extract_Line_Num(inPoint))
            self.eventManager.add_Event(exeTrace)
            addExePoint = True
            
        elif on == False and off == False:
            addExePoint = False
        else:
            addExePoint = False

        return addExePoint

    def exe_Point_Finder(self, trace): #This is really messy. Sorry. I will definitely need to refactor in the future
        symbolStack = []
        exePointList = []
        otherList = []
        currentSymbol = ''
        topSymbol = ''
        exe = ""
        exePoint = " "
        on = False
        off = False
        counter = 0
        
        for i in trace:
            currentSymbol = i
            exePoint = exePoint + currentSymbol
            if i == '{' or i == '[' or i == '(':
                symbolStack.append(i)
            elif i == '}' or i == ')' or i == ']':
                if self.is_empty(symbolStack) == False:
                    topSymbol = symbolStack.pop()
                    if i == '}' and topSymbol != '{':
                        continue
            elif i == ',':
                otherList.append(exePoint)
                if len(symbolStack) == 0:
                    for thing in otherList:
                        exe = exe + thing
                        
                    if "startTraceNow" in exe:
                        on = True
                        exe = ""
                        exePoint = ""
                        otherList = []
                    elif "endTraceNow" in exe:
                        off = True
                        return
                    else:
                        flag = self.verify_Exe_Point(on, off, exe)
                        if flag == True:
                            exe = ""
                            exePoint = ""
                            otherList = []
                        else:
                            on = False
                            exe = ""
                            exePoint = ""
                            otherList = []
                else:
                    exePoint = ""
            else:
                continue

def is_empty(structure):
    if structure:
        return False
    else:
        return True

def codeSplitter(code):

    studentCode = []

    code = code.split("startTraceNow();")
    newCode = code[1].split("endTraceNow();")

    executedCode = newCode[0]

    exeCodeList = executedCode.split("\\n")

    flag = False
    counter = 0 
    
    while flag != True:
        if exeCodeList[counter] == "" or exeCodeList[counter] == " ":
            flag = False
            counter = counter + 1
        elif exeCodeList[counter] != "":
            flag = True

    for x in range(counter, len(exeCodeList)):
        temp = exeCodeList[x]
        temp = "".join(temp.split())

        if is_empty(temp):
            studentCode.append("newline")
        else:
            studentCode.append(exeCodeList[x])

    return studentCode


def codeAnalyzer(code, firstTrace):
    
    codeToViz = []    
    codeToViz = codeSplitter(code)

    traceAnalyzer = TraceAnalyzer()

    execute = traceAnalyzer.handleEverything(codeToViz, firstTrace)

    


wholeTrace = wholeTrace[1:]
    
codeAnalyzer(userCode, wholeTrace)

    

