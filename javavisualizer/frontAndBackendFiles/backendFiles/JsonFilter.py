#Author: Kyle Reinholt
#Refactored Author : Medha Baidya
#Date: 6/25/15
#Program: Json Filter
#Purpose: To extract execution points from the json trace produced from InMemory.java that are intended for visualization
#Documentation: There is an example at the very end of this file. The in-code documentation for this filter is not very extravagent.
#The seperateAndFilterTrace() function contain a flow-explanation of what is happening in this program. 
import os
import sys
sys.path.append('./..')
import subprocess
import config


def generateBackendTrace(jUnitTestFile, filesPath, peruserFilesPath, studentfilename):


    #filesPath = ""
    #jUnitTestFile = "test.java"
    TestFile = open(filesPath+jUnitTestFile , 'r')
    raw_code = TestFile.read()

    raw_code = raw_code.replace("\n","\\n" + "\n")
    raw_code = raw_code.replace("\t","\\t")

    lines = raw_code.split("\n");
    jUnitTest = ""

    for line in lines:
        jUnitTest = jUnitTest + line


    jUnitTest = jUnitTest.replace("\"", "\\" + "\"")
    #print jUnitTest

    #peruserFilesPath = "/Your/Path/To/cp/traceprinter/"
    #studentfilename = "output.txt"

    if not os.path.exists(peruserFilesPath ):
       os.makedirs(peruserFilesPath)

    generateTrace = open(peruserFilesPath+studentfilename, 'w')
    generateTrace.write("{" + "\n" + '"' + "usercode" + '"' + ':' + '"' + jUnitTest + '"' + ',' + "\n" + '"' + "options" + '"' + ':' + '{' + '}' + ',' + "\n" + '"' + "args" 		+ '"' + ':' + '[' + ']' + ',' + "\n" + '"' + "stdin" + '"' + ':' + '"' + '"' + "\n" + '}')
    generateTrace.close()

    #This shell command should work after the paths for the java tools and
    # traceprinter packages have been correctly modified.

    command = config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/java/bin/java -cp .:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/cp:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/java/lib:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/cp/javax.json-1.0.jar:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/cp/javax.json-1.0.4.jar:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/java/lib/:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/java/lib/tools.jar:" + config.base_path + config.submodule_path + "/javavisualizer/frontAndBackendFiles/backendFiles/cp/traceprinter traceprinter.InMemory < " + peruserFilesPath+studentfilename


    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)

    #Launch the shell command:
    output = process.communicate()

    backend_trace = output[0]
    return backend_trace

#This function calls the functions necessary to completely execute the program. 
def seperateAndFilterTrace(jUnitTestFile, filesPath, peruserFilesPath, studentfilename):

    #This takes the .java file from the OpenDSA backend, formats the file into a json object,
    # inserts the json object into the traceprinter to generate the 50,000 character+ json object
    codeAndTrace = generateBackendTrace(jUnitTestFile, filesPath, peruserFilesPath, studentfilename)
    #After the trace is generated, it is split into two pieces, the code section and trace section of the json
    # object.
    splitter = '"' + "trace" + '"' + ':'
    userCode, wholeTrace = codeAndTrace.split(splitter)
    #print wholeTrace

    #The first character is removed from the trace section because the bracket at the beginning of the trace
    # was causing problems in the execution point locater function.
    wholeTrace = wholeTrace[1:]
    #Finally, the two pieces of the json object are anaylyzed by means of extracting all unwanted code
    # and execution traces. There is functionality within the codeAnalyzer that outputs the results to
    # a "ready-to-go" javaScript file. "ready-to-go" meaning you just have to include the <div> in
    # html file to display the executionVisualizer!
    entireJSFile = codeAnalyzer(userCode, wholeTrace)


    return entireJSFile

class TraceAnalyzer(object):

    def handleEverything(self, userCode, inTrace):
        # making the exceutable events consistent with user code text.
        #consistent_events = modifySelectedEventList(clean_Events,4)

        #At this point, everything is ready for output. The printToFile string
        # contains all of the information necessary for the javaScript file.
        # Its about 20 lines down
        orig_stdout = sys.stdout
        #f = file('codeScript.js', 'w')
        #sys.stdout = f

        f = ''
        first = "var testvisualizerTrace = {\"code\":\""

        code = ""

        for x in range (0,len(userCode)):
            if userCode[x] == "newline":
                code = code + "\\n" + " "
            else:
                code = code + userCode[x] + "\\n"
        second = "\",\"trace\":["

        traceWithoutLine = self.find_executable_trace(inTrace)
        traceWithoutLine = self.clean_repeated_trace(traceWithoutLine)
        traceWithoutLine = self.clean_stack_trace(traceWithoutLine)
        traceWithoutLine = self.clean_heap_trace(traceWithoutLine)
        index = 1;
        trace = []
        for traceElement in traceWithoutLine:
            traceLine = traceElement
            firstStr = traceLine.split('"line":')
            end=firstStr[1].split('"stack_to_render"')
            stringStepLineReturned = firstStr[0] + '"line":' + str(index) + ',"stack_to_render"' + end[1]
            trace.append(stringStepLineReturned)
            index = index+1

        final_trace = ''

        for y in trace:
            final_trace = final_trace+''+y
        final_trace = final_trace +"],\"userlog\":\"Debugger VM maxMemory: 807M \\n \"}"
        final_trace = final_trace + "\n" + "$(document).ready(function() { \n \n \t var testvisualizer = new ExecutionVisualizer('testvisualizerDiv', testvisualizerTrace,{embeddedMode: false, lang: 'java', heightChangeCallback: redrawAllVisualizerArrows}); \n \n \tfunction redrawAllVisualizerArrows() { \n \n \t \t if (testvisualizer) testvisualizer.redrawConnectors(); \n \t } \n \n $(window).resize(redrawAllVisualizerArrows); \n});"


        #String that contains everything for the javascript file
        # Maybe just send string to front end and write to file in
        # a directory accessible by the OpenDSA frontend?
        f = first + code + second + final_trace
        #printToFile = first + code + second + final_trace


        return f
        #return printToFile

    def is_empty(self, any_structure):
        if any_structure:
            return False
        else:
            return True

    def index_containing_substring(self, the_list, substring):
        for i, s in enumerate(the_list):
            if substring in s:
                return i
        return -1

    def last_index_startTrace(self, the_list, substring):
        indices = [i for i, s in enumerate(the_list) if substring in s]
        return indices.pop()


    def clean_trace_based_on_num(self, the_list, line_start, line_end):
        cleanTraceList=[]
        for traceElement in the_list:
            trace_line = self.find_line_num(traceElement)
            if line_start <= trace_line <= line_end :
                cleanTraceList.append(traceElement)

        return cleanTraceList


    def find_between(self,  s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_between_right(self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_line_num(self, stringStepLine):
        lineNum = self.find_between(stringStepLine, '"line":', ',')
        lineNum = lineNum.strip()
        return lineNum

    def set_line_num(self, stringStepLine, i):
        first = stringStepLine.split('"line":')
        end = first[1].split('"stack_to_render"')
        stringStepLineReturned = first + '"line":' + i + ',"stack_to_render"' + end
        return stringStepLine

    def clean_repeated_trace(self, clean_trace):
        prevHeapContent = ''
        prevStkContent = ''

        for trace in clean_trace:
            currHeap = self.get_heap_content(trace)
            currStack = self.get_stack_content(trace)

            if currHeap==prevHeapContent and prevStkContent == currStack:
                clean_trace.remove(trace)

            prevStkContent = currStack
            prevHeapContent = currHeap

        return clean_trace

    def find_executable_trace(self, trace):
        traceOne = trace.split("stdout")

        brackets = '{"'
        traceStepList = [traceElement.strip(brackets) for traceElement in traceOne]

        stdout  = '{"stdout"'
        traceStepList = [stdout + traceE for traceE in traceStepList]


        stringStartTrace = 'startTraceNow'
        indexStartTrace = self.last_index_startTrace(traceStepList, stringStartTrace)

        stringEndTrace = 'endTraceNow'

        indexEndTrace = self.index_containing_substring(traceStepList, stringEndTrace)


        traceStepList = traceStepList[indexStartTrace+1: indexEndTrace]

        line_Start = self.find_line_num(traceStepList[0])
        line_End = self.find_line_num(traceStepList[len(traceStepList)-1])

        clean_trace = self.clean_trace_based_on_num(traceStepList, line_Start, line_End)
        return clean_trace

    def clean_stack_trace(self, clean_trace):
        stackStr = "stack_to_render\":["
        stackMid = "},{"
        stackEnd = "],\"globals\""
        index = 0;
        for curr_trace in clean_trace:
            curStack = curr_trace.split(stackStr)

            curStackE = curStack[1].split(stackEnd)
            apendStack = self.find_between(curr_trace, stackStr, stackMid )
            clean_trace[index] = curStack.pop(0) + stackStr + apendStack + '}'+ stackEnd + curStackE.pop()
            # print clean_trace[index]
            index = index + 1

        clean_trace.pop(0)
        return clean_trace

    def get_heap_content(self, one_trace_instance):
        heap_str = '"heap":{'
        heap_end = '}'
        curHeap = self.find_between(one_trace_instance, heap_str, heap_end)
        return curHeap

    def get_stack_content(self, one_trace_instance):
        stack_str = '"encoded_locals":'
        stack_end = "},"
        stack = self.find_between(one_trace_instance, stack_str, stack_end)
        return stack

    def clean_heap_trace(self, clean_trace):
        heap_str = '"heap":{'
        heap_end = '}'
        strSplitter = ',["e",'
        traceEndRemainsStr = "}},"
        new_trace = []
        heap_objects = 4
        for curr_trace in clean_trace:
             curHeap = self.get_heap_content(curr_trace)
             traceTopRemains = curr_trace.split('"heap":{')
             traceEndRemains = traceTopRemains[1].split("}},")

             if curHeap == '' or curHeap == ' ' or curHeap == '{':
                 new_trace.append(str(traceTopRemains[0]) + '"heap": {'+traceEndRemainsStr)
                 continue

             heapSplit = curHeap.split(strSplitter)
             cleanedHeap = ''
             totalHeap = []
             heapPart1 = []
             numLst = []
             heapPart2 = []

             idex = 0;
             for heap in heapSplit:
                 idex += 1
                 print heap
                 num = ''
                 print num
                 print idex
                 if idex != 1:
                    num = heap[0:1]
                    num = '["e",'+ num+'],'
                    numLst.append(num)
                    heap = heap[4:len(heap)]
                 else:
                    heap = heap[0:len(heap)]

                 print numLst

                 heapPart = heap.split('"Link",')

                 if len(heapPart)>1:
                     heapPart1.append(heapPart.pop(0))
                     heapPart2.append(str(heapPart.pop())+'],')
                 else:
                     #heapPart2.append((str(heapPart2.pop()).rstrip(','))+'],')
                     heapPart1.append(str(heapPart.pop(0)))
                 print numLst, heapPart1, heapPart2

             while len(heapPart1) > 0:
                 if len(heapPart2) > 0:
                     cleanedHeap = cleanedHeap + ''+heapPart1.pop(0) + '"Link",' + numLst.pop(0) + heapPart2.pop(0)
                     print numLst, heapPart1, heapPart2
                     print cleanedHeap
                 else:
                     cleanedHeap = cleanedHeap +''+heapPart1.pop(0)

             print cleanedHeap
             totalHeap.append(cleanedHeap)
             heapContent = ''.join(totalHeap)
             new_trace.append(str(traceTopRemains[0]) + '"heap": {'+ heapContent+traceEndRemainsStr)

        return new_trace


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

    exeCodeList = executedCode.split(";")
    if exeCodeList[len(exeCodeList)-1] == '\\t' or exeCodeList[len(exeCodeList)-1] == '\\n':
        exeCodeList.pop()

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

    return execute

#This is an example of how to use the seperateAndFilterTrace() function. This 
#function initiates everything. Include this in your python code with the proper 
#parameters to get expected results. myTest is a string that contains the entire js file contents for visualizing code.
#Send this string to the correct frontend directory, make a javaScript file and only containing myTest, then include the
# proper links and scripts in the html page and you should be good to go. 

#myTest = seperateAndFilterTrace("studentpntrequalspntrPROG.java", "/vagrant/OpenDSA-server/ODSA-django/openpop/build/pntrtest/pntrequalspntrPROG/Medha/", "/vagrant/OpenDSA-server/ODSA-django/openpop/build/pntrtest/pntrequalspntrPROG/", "Medha")
#for local debugging
#myTest = seperateAndFilterTrace("studentpntrequalspntrPROG.java", "/vagrant/OpenDSA-DevStack/OpenDSA-server/ODSA-django/openpop/build/pntrtest/pntrequalspntrPROG/Medha/", "/vagrant/OpenDSA-DevStack/OpenDSA-server/ODSA-django/openpop/build/pntrtest/pntrequalspntrPROG/", "Medhaa")
#filterJson.close()
#myTest = seperateAndFilterTrace("studentpntrequalspntrPROG.java", "/vagrant/OpenDSA-server/ODSA-django/openpop/build/pntrtest/pntrequalspntrPROG/Medha/", "/vagrant/OpenDSA-server/ODSA-django/openpop/build/pntrtest/pntrequalspntrPROG/", "Medhaa")
#print myTest
