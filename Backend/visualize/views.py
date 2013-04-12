# Create your views here.

from django.http import HttpResponse

def index(request , data):
    #!/usr/bin/env python

	# Sally
	# 1- get the code written by the student
	# 2- put it in the value_entered field in the foo.xml file
	# 3- run the java command given by prof. Tom
	#  //http://stackoverflow.com/questions/1880198/how-to-execute-shell-command-in-java-script
	#  //var shell = WScript.CreateObject("WScript.Shell");
	#  //shell.Run("command here");
	#  //java -cp jhavepop-support.jar:jdom.jar:jaxen.jar:. exe.memorymanager.memorymanager foobar X foo.xml 
	# 4-get the .sho file and run the python code while passing .sho file
	# 5- Redirect to the visulization page

	import xml.etree.ElementTree as xml # for xml parsing
	import shlex # for strings splitting
	import re # for special characters escaping

	tokensFile = open('forjsav', 'w')
	tree = xml.parse('foobar.sho') # parse an XML file by name
	#tree = xml.parse('C:\\phd\\Research\\JhavePOP\\jhavepop-standalone\\foobar.sho')
	rootElement = tree.getroot()

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

	######################################### Building Java script code ##############################################################################
	# Next we will process the tokens file: reproducing the same function I've already written in Javascript
	#Insha ALLAH :) From the JhavePOPParsingFileContent build the JSAV slide show 
	javaScriptOutputFile = open ('JSAVFromJhave.js', 'w') # This is going to be the output javascript file
	tokensFile = open('forjsav' , 'r')
	lines = tokensFile.readlines()

	# Visulization function definition
	javaScriptOutputFile.write('(function ($) {\n')

	# Visulization Variables 
	topIndent = 50
	leftIndent = 450
	nodeGap = 40
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
	javaScriptOutputFile.write('var headPointer;\n')
	javaScriptOutputFile.write('var tailPointer;\n')
	javaScriptOutputFile.write('var otherPointers = [];\n')
	javaScriptOutputFile.write('var headLabel;\n')
	javaScriptOutputFile.write('var tailLabel ;\n')
	javaScriptOutputFile.write('var otherPointersLabels = [];\n')



	# Visulization definition to be written to the java script file
	javaScriptOutputFile.write('var av = new JSAV("container");\n')
	javaScriptOutputFile.write('av.settings.add("speed", {"type": "range", "value": "10", "min": 1, "max": 20, "step": 1});\n')
	#Here is the linked list
	javaScriptOutputFile.write('var l = av.ds.list({top: ('+ str(topIndent)+'), left: '+ str(leftIndent)+', nodegap: '+ str(nodeGap)+'});\n')


	for line in lines :
		#javaScriptOutputFile.write('l.layout();\n')
		#setting the defaults back
		strokeColor= "'black'"
		strokeWidth ='2'
		currentToken= line.rstrip() # trimming the end of line
		currentTokenSplitted = shlex.split(currentToken) # in some cases we need to split the token if there are white spaces""
		
		# new snap shot --> mapped to a new slide
		if currentToken == 'slide': 
			javaScriptOutputFile.write('av.step();\n')
			while nodesCount!=0 :
			  javaScriptOutputFile.write('l.remove(0);\n')
			  nodesCount = nodesCount-1

			javaScriptOutputFile.write('l.layout({center: false});\n')
			if slideNumber>0 :
				javaScriptOutputFile.write('headPointer.hide();\n')
				javaScriptOutputFile.write('tailPointer.hide();\n')
				javaScriptOutputFile.write('headLabel.hide();\n')
				javaScriptOutputFile.write('tailLabel.hide();\n')
				j=0
				# hide all other pointers and labels
				while otherPointersCount !=0 :
				   javaScriptOutputFile.write('otherPointers[ '+str(j)+'].hide();\n')
				   javaScriptOutputFile.write('otherPointersLabels['+str(j)+'].hide();\n')
				   otherPointersCount = otherPointersCount-1
			javaScriptOutputFile.write('av.umsg("Slide '  + str(slideNumber)+'");\n')
			slideNumber= slideNumber +1;
			javaScriptOutputFile.write('l.layout();\n')
		# End of new snap shot

		# Adding a new node
		elif len(currentToken) == 1 and lines[i+1].rstrip() != 'remove':
			javaScriptOutputFile.write('l.addLast("'+ currentToken +'");\n')
			javaScriptOutputFile.write('l.layout();\n')
			if lines[i+1].rstrip() == 'nred':
				javaScriptOutputFile.write('l.get('+ str (nodesCount) +').highlight();\n')
			nodesCount= nodesCount+ 1
			javaScriptOutputFile.write('l.layout();\n')
		# End of adding a new node

		# Removing a node by dimming it
		elif len(currentToken) == 1 and lines[i+1].rstrip() == 'remove':
			 javaScriptOutputFile.write('l.addLast("'+ currentToken +'");\n')
			 javaScriptOutputFile.write('l.get(' + str(nodesCount) +').css({backgroundColor: "#808080"});\n')
			 javaScriptOutputFile.write('l.layout();\n')
			 nodesCount= nodesCount+1
			 javaScriptOutputFile.write('l.layout();')
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
			javaScriptOutputFile.write('headPointer = av.g.line('+ str(x1) +' , 10,'+ str(x2) +', 50,{"arrow-end": "classic-wide-long", "opacity": 0, "stroke":'+ strokeColor+',"stroke-width":'+ str(strokeWidth)+'});\n')
			javaScriptOutputFile.write('headPointer.show();\n')
			leftLabelIndent= leftIndent + nextNodeIndent *int(pointsTo) -8
			javaScriptOutputFile.write('headLabel = av.label("head", {before: l, left:  '+ str(leftLabelIndent)+ ' , top: 0 });\n')
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
			javaScriptOutputFile.write('tailPointer = av.g.line('+ str(x1) +' , 10,'+ str(x2) +', 50,{"arrow-end": "classic-wide-long", "opacity": 0, "stroke":'+ strokeColor+',"stroke-width":'+ str(strokeWidth)+'});\n')
			javaScriptOutputFile.write('tailPointer.show();\n')
			leftLabelIndent= leftIndent + nextNodeIndent *int(pointsTo) + nodeGap-5
			javaScriptOutputFile.write('tailLabel = av.label("tail", {before: l, left:  '+ str(leftLabelIndent)+ ' , top: 0 });\n')
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
			javaScriptOutputFile.write('otherPointers['+ str(otherPointersCount)+'] = av.g.line('+ str(x1) +' , 10,'+ str(x2) +', 50,{"arrow-end": "classic-wide-long", "opacity": 0, "stroke":'+ strokeColor+',"stroke-width":'+ str(strokeWidth)+'});\n')
			javaScriptOutputFile.write('otherPointers['+str(otherPointersCount)+'].show();\n')
			leftLabelIndent= leftIndent + nextNodeIndent *int(pointsTo) +nodeGap-13
			javaScriptOutputFile.write('otherPointersLabels['+str(otherPointersCount)+'] = av.label("'+currentTokenSplitted[1]+'", {before: l, left:  '+ str(leftLabelIndent)+ ' , top: 0 });\n')
			otherPointersCount = otherPointersCount+1;
		# End of Other pointers
		
		i=i+1

	# End of the visulization    
	javaScriptOutputFile.write('av.recorded();\n')
	# end of the function
	javaScriptOutputFile.write('}(jQuery));\n')
	# close the tokens and the javascript files
	tokensFile.close()
	javaScriptOutputFile.close()

	return HttpResponse(data)
