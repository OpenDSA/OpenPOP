jsonFilter.py
=============
This is a clone of the jsonFilter.java
I am currently translating the code from java to python. The code must be in python because the OpenDSA backend is written in python. I am still running tests on the jsonFilter.py, it is only capable of extracting the execution points between startTraceNow and endTraceNow. The eventManager functionality needs to be written and the userCode analyzer must be added to the .py file still. This README will be updated as the contents of jsonFilter.py are updated.  

jsonFilter.java
===============

The SampleBackEndTrace.txt contains an example of what the trace input (created from InMemory.java from the traceprinter package) would look like for the 
jsonFilter. 

The SampleFilteredTrace.js is what the ouput looks like after SampleBackEndTrace.txt has been passed 
through the jsonFilter. The ExecutionVisualizer functionality is from Philip Guo's Online Python Tutor (https://github.com/pgbovine/OnlinePythonTutor). 

jsonFilter.java reads in the backEndTrace as a string and removes unwanted execution points and outputs the javaScript 
file that is used by the HTML file to display the visualization of the generated trace. Two steps in one hopefully!
Time will tell... 
