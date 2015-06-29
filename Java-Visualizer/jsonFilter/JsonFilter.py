#Author: Kyle Reinholt
#Date: 6/25/15
#Program: Json Filter
#Purpose: To extract execution points from the json trace produced from InMemory.java that are intended for visualization

with open('jsontrace.txt','r') as f:
    read_data = f.read()

f.closed

splitter = '"' + "trace" + '"' + ':'

userCode, trace = read_data.split(splitter)

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
    
    def get_Events(index):
        return self.listOfEvents[index]

    def add_Event(self, event):
        self.listOfEvents.append(event)

    def print_Events(self):
        if (len(self.listOfEvents) == 0):
            print("List of events is empty")
        else:
            for x in range(0, len(self.listOfEvents)):
                tempEvent = self.listOfEvents[x]
                print(tempEvent.trace)

class TraceAnalyzer(object):

    def __init__(self, trace):
        self.__inTrace = trace 
        self.eventManager = EventManager()
        self.exe_Point_Finder
        print "Object Created"
        
    @property
    def trace(self):
        return self.__inTrace

    def printMe(self):
        doop = self.eventManager.print_Events
        doop()
        
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
        
        print("String: ", line)
        line = [int(s) for s in line.split() if s.isdigit()]
        print line
        return line[0]

    def verify_Exe_Point(self, on, off, inPoint):

        print("Reached verify_exe")
        print(on)
        print(off)
        addExePoint = False
        exeTrace = Event()

        if on == True and off == False:
            exeTrace.set_Event(inPoint)
            exeTrace.set_Line(self.extract_Line_Num(inPoint))
            self.eventManager.add_Event(exeTrace)
            addExePoint = True
            print("addExePoint = True")
        elif on == False and off == False:
            addExePoint = False
        else:
            addExePoint = False

        return addExePoint

    def exe_Point_Finder(self): #This is really messy. Sorry. I will definitely need to refactor in the future
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
        
        for i in self.__inTrace:
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

                    print("on is" , on)
                    if "startTraceNow" in exe:
                        print("StartTraceNow found")
                        print(exe)
                        on = True
                        exe = ""
                        exePoint = ""
                        otherList = []
                    elif "endTraceNow" in exe:
                        off = True
                        return
                    else:
                        flag = self.verify_Exe_Point(on, off, exe)
                        print("flag is", flag)
                        if flag == True:
                            print(exe)
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

        

trace = trace[1:]

traceAnalyzer = TraceAnalyzer(trace)
blah = traceAnalyzer.exe_Point_Finder
blah()

blah2 = traceAnalyzer.printMe
blah2()

print("made it here") 
    
"""def modifyLineNums(userCode):
lineNum = 0
eventNum = 0"""

    
"""
test = Event()
test2 = Event()
test3 = Event()

testManager = EventManager()

test.set_Event("First Test")
test.set_Line(14)
test2.set_Event("Seond Test")
test2.set_Line(14)
test3.set_Event("Third Test")
test3.set_Line(14)

testManager.add_Event(test)
testManager.add_Event(test2)
testManager.add_Event(test3)
testManager.print_Events()
"""

        

