# Create your views here.

from django.http import HttpResponse
import xml.etree.ElementTree as xml # for xml parsing
import shlex # for strings splitting
import re # for special characters escaping
import os
#from subprocess import call
#import pdb; pdb.set_trace()
def visualize_code(data):
    print "I am in the begining of visualizing the code"
    print data
    ##################### Put the student code in the value_entered and create an XML file  to be feed to the java command####################################### 
    # start creating foo.xml
    foo = open('/home/OpenPOP/Backend/visualize/foo.xml', 'w')
    foo.write("""<?xml version="1.0" encoding="UTF-8"?>
<input_panel><textarea><label_line>Enter your Java or C++ source code below:</label_line><default_field>Remove all A's from the list
// gridsize 1 6 java 0.3
Node head = Utils.createList( 'A','A','B','A','C','A',"tail" );
Node p = null; // 0 2
</default_field><value_entered>\n"""+ data +"""\n""" + """</value_entered></textarea></input_panel>""")
    
    foo.close()
    os.chdir("/home/OpenPOP/Backend/visualize")
    print os.getcwd()
    ####################### Run the Java command to produce the snap shots file ##########################################################################################
    print "before the java call"
    os.system(" java -cp jhavepop-support.jar:jdom.jar:jaxen.jar:. exe.memorymanager.memorymanager foobar X foo.xml")
    
    ################################################## Parsing the .sho (snap shots) file and writting down the tokens file #################################################

    
    tree = xml.parse('/home/OpenPOP/Backend/visualize/foobar.sho') # parse an XML file by name

    rootElement = tree.getroot()
    tokensFile = open('/home/OpenPOP/Backend/visualize/forjsav', 'w')

    currentState = 'start' # To track if the current node is a pointer or a node in the linked list

    # looping all over the file nodes and attributes
    for node in rootElement.iter():
    # It's a new snap then it is a new JSAV slide (check with Prof Cliff)
       
        if node.tag == 'snap':
          tokensFile.write('slide\n') # This will map to a new slide in JSAV
          
    # This is a pointer [head , tail or anything that is not head or tail]
        if node.tag == 'ref_label':
          tokensFile.write('pointer ' + node.text + '\n')
          currentState = node.tag # Keep track of the current node
         
    # This is a data node
        if node.tag == 'data':
          tokensFile.write(node.attrib['value']+ '\n')
          currentState = node.tag # Keep track of th current node
          
    # A next node
        if node.tag == 'next':
          currentState = node.tag # Keep track of th current node
    # This is a pointer
        if node.tag == 'arrow':
            if currentState=='ref_label' :
              if node.attrib['line_color'] == '#FF0000' : # The pointer color
                 tokensFile.write('pred\n')
              if 'col' in node.attrib :
                 tokensFile.write('points to ' + node.attrib['col']+ '\n')

    # Handling node color if red then it will be highlight it
        if node.tag == 'box' and currentState=='data' :
          if node.attrib['line_color'] == '#FF0000':
            tokensFile.write('nred\n')
            currentState = 'start'

    # A dimmed node and pointer will be removed in the JSAV        
          if node.attrib['line_color'] == '#BBBBBB' and node.attrib['fill_color'] == '#F5F5F5'  and currentState=='data' : # node dimmed to be removed
            tokensFile.write( 'remove\n')
    tokensFile.close()

    ######################################### Building Java script code that visualizes student code ##############################################################################
    # Next we will process the tokens file: reproducing the same function I've already written in Javascript
    #Insha ALLAH :) From the JhavePOPParsingFileContent build the JSAV slide show 
    #javaScriptOutputFile = open ('JSAVFromJhave.js', 'w') # This is going to be the output javascript file
    tokensFile = open('forjsav' , 'r')
    lines = tokensFile.readlines()

    # Visulization function definition
    javaScriptOutput =  '(function ($) {\n'
    # Visulization Variables 
    topIndent = 50
    leftIndent = 450
    nodeGap = 40
    NodeWidth = 40
    NodeWidth = 40
    nextNodeIndent = NodeWidth + nodeGap
    pointsTo=0
    slideNumber=0
    strokeColor= 'black'
    strokeWidth ='2'
    nodesCount=0;
    otherPointersCount=0;
    i=0 # this iterator is used to have access to the next lines to the current line


    #Pointers : head , tail , other pointers and their labels
    javaScriptOutput = javaScriptOutput + 'var headPointer;\n'
    javaScriptOutput = javaScriptOutput + 'var tailPointer;\n'
    javaScriptOutput = javaScriptOutput + 'var otherPointers = [];\n'
    javaScriptOutput = javaScriptOutput + 'var headLabel;\n'
    javaScriptOutput = javaScriptOutput + 'var tailLabel ;\n'
    javaScriptOutput = javaScriptOutput + 'var otherPointersLabels = [];\n'



    # Visulization definition to be written to the java script file
    javaScriptOutput = javaScriptOutput + 'var av = new JSAV("container");\n'
    #javaScriptOutput = javaScriptOutput + 'av.settings.add("speed", {"type": "range", "value": "5", "min": 1, "max": 20, "step": 1});\n'
    #Here is the linked list
    javaScriptOutput = javaScriptOutput + 'var l = av.ds.list({top: ('+ str(topIndent)+'), left: '+ str(leftIndent)+', nodegap: '+ str(nodeGap)+'});\n'


    for line in lines :
        #javaScriptOutput = javaScriptOutput + ('l.layout();\n')
        #setting the defaults back
        strokeColor= "'black'"
        strokeWidth ='2'
        currentToken= line.rstrip() # trimming the end of line
        currentTokenSplitted = shlex.split(currentToken) # in some cases we need to split the token if there are white spaces""
        
        # new snap shot --> mapped to a new slide
        if currentToken == 'slide':
            if slideNumber>1:
              javaScriptOutput = javaScriptOutput + 'av.step();\n'
            while nodesCount!=0 :
              javaScriptOutput = javaScriptOutput + 'l.remove(0);\n'
              nodesCount = nodesCount-1

            javaScriptOutput = javaScriptOutput + 'l.layout({center: false});\n'
            if slideNumber>0 :
                javaScriptOutput = javaScriptOutput + 'headPointer.hide();\n'
                javaScriptOutput = javaScriptOutput + 'tailPointer.hide();\n'
                javaScriptOutput = javaScriptOutput + 'headLabel.hide();\n'
                javaScriptOutput = javaScriptOutput + 'tailLabel.hide();\n'
                j=0
                # hide all other pointers and labels
                while otherPointersCount !=0 :
                   javaScriptOutput = javaScriptOutput + 'otherPointers[ '+str(j)+'].hide();\n'
                   javaScriptOutput = javaScriptOutput + 'otherPointersLabels['+str(j)+'].hide();\n'
                   otherPointersCount = otherPointersCount-1
            #javaScriptOutput = javaScriptOutput + 'av.umsg("Slide '  + str(slideNumber)+'");\n'
            slideNumber= slideNumber +1;
            javaScriptOutput = javaScriptOutput + 'l.layout();\n'
        # End of new snap shot

        # Adding a new node
        elif len(currentToken) == 1 and lines[i+1].rstrip() != 'remove':
            javaScriptOutput = javaScriptOutput + 'l.addLast("'+ currentToken +'");\n'
            javaScriptOutput = javaScriptOutput + 'l.layout();\n'
            if lines[i+1].rstrip() == 'nred':
                javaScriptOutput = javaScriptOutput + 'l.get('+ str (nodesCount) +').highlight();\n'
            nodesCount= nodesCount+ 1
            javaScriptOutput = javaScriptOutput + 'l.layout();\n'
        # End of adding a new node

        # Removing a node by dimming it
        elif len(currentToken) == 1 and lines[i+1].rstrip() == 'remove':
             javaScriptOutput = javaScriptOutput + 'l.addLast("'+ currentToken +'");\n'
             javaScriptOutput = javaScriptOutput + 'l.get(' + str(nodesCount) +').css({backgroundColor: "#808080"});\n'
             javaScriptOutput = javaScriptOutput + 'l.layout();\n'
             nodesCount= nodesCount+1
             javaScriptOutput = javaScriptOutput + 'l.layout();'
        # End of Removing a node by dimming it

        # Head pointer
        elif currentToken == 'pointer head':
            if lines[i+1].rstrip() == 'pred':
                pointsTo = shlex.split(lines[i+2].rstrip())[2] #contains the column it should points  to  "points to 0"
                strokeColor="'red'"
                strokeWidth= "3"
            else:
                pointsTo = shlex.split(lines[i+1].rstrip())[2] #contains the column it should points  to  "points to 0"
            x1 = leftIndent + (nextNodeIndent * int (pointsTo)) - 20.0
            x2 = leftIndent + nextNodeIndent * int(pointsTo)
            javaScriptOutput = javaScriptOutput + 'headPointer = av.g.line('+ str(x1) +' , 10,'+ str(x2) +', 50,{"arrow-end": "classic-wide-long", "opacity": 0, "stroke":'+ strokeColor+',"stroke-width":'+ str(strokeWidth)+'});\n'
            javaScriptOutput = javaScriptOutput + 'headPointer.show();\n'
            leftLabelIndent= leftIndent + nextNodeIndent *int(pointsTo) -8
            javaScriptOutput = javaScriptOutput + 'headLabel = av.label("head", {before: l, left:  '+ str(leftLabelIndent)+ ' , top: 0 });\n'
        # End of head pointer

        # Tail Pointer
        elif currentToken == 'pointer tail':
            if lines[i+1].rstrip() == 'pred':
                pointsTo = shlex.split(lines[i+2].rstrip())[2] #contains the column it should points  to  "points to 0"
                strokeColor="'red'"
                strokeWidth= "3"
            else:
                pointsTo = shlex.split(lines[i+1].rstrip())[2] #contains the column it should points  to  "points to 0"
            x1 = leftIndent + (nextNodeIndent * int (pointsTo)) + nodeGap-23
            x2 = leftIndent + nextNodeIndent * int(pointsTo)+ nodeGap
            javaScriptOutput = javaScriptOutput + 'tailPointer = av.g.line('+ str(x1) +' , 10,'+ str(x2) +', 50,{"arrow-end": "classic-wide-long", "opacity": 0, "stroke":'+ strokeColor+',"stroke-width":'+ str(strokeWidth)+'});\n'
            javaScriptOutput = javaScriptOutput + 'tailPointer.show();\n'
            leftLabelIndent= leftIndent + nextNodeIndent *int(pointsTo) + nodeGap-5
            javaScriptOutput = javaScriptOutput + 'tailLabel = av.label("tail", {before: l, left:  '+ str(leftLabelIndent)+ ' , top: 0 });\n'
        # End of tail pointer

        # Other pointers
        elif currentTokenSplitted[0] == 'pointer' and (currentTokenSplitted[1] != 'head' or currentTokenSplitted[1] != 'tail' ):
            if lines[i+1].rstrip() == 'pred':
                if shlex.split(lines[i+2].rstrip())[0] == "points":  # The column to which it points to is specified
                    pointsTo = shlex.split(lines[i+2].rstrip())[2]
                else :
                    pointsTo=-3
                strokeColor = "'red'"
            else :
                if shlex.split(lines[i+2].rstrip())[0] == "points":  # The column to which it points to is specified
                    pointsTo = shlex.split(lines[i+2].rstrip())[2]
                else :
                    pointsTo=-3
            x1 = leftIndent + (nextNodeIndent * int (pointsTo)) + nodeGap-23
            x2 = leftIndent + nextNodeIndent * int(pointsTo)+ nodeGap  
            javaScriptOutput = javaScriptOutput + 'otherPointers['+ str(otherPointersCount)+'] = av.g.line('+ str(x1) +' , 10,'+ str(x2) +', 50,{"arrow-end": "classic-wide-long", "opacity": 0, "stroke":'+ strokeColor+',"stroke-width":'+ str(strokeWidth)+'});\n'
            javaScriptOutput = javaScriptOutput + 'otherPointers['+str(otherPointersCount)+'].show();\n'
            leftLabelIndent= leftIndent + nextNodeIndent *int(pointsTo) +nodeGap-13
            javaScriptOutput = javaScriptOutput + 'otherPointersLabels['+str(otherPointersCount)+'] = av.label("'+currentTokenSplitted[1]+'", {before: l, left:  '+ str(leftLabelIndent)+ ' , top: 0 });\n'
            otherPointersCount = otherPointersCount+1;
        # End of Other pointers
        
        i=i+1

    # End of the visulization    
    javaScriptOutput = javaScriptOutput + 'av.recorded();\n'
    # $('#reset').click(reset); end of the function
    javaScriptOutput = javaScriptOutput + '}(jQuery));\n'
    # close the tokens and the javascript files
    tokensFile.close()
    #javaScriptOutputFile.close()
    return  javaScriptOutput
