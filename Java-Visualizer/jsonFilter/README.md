jsonFilter.py
=============
This is a python version of the jsonFilter.java

I originally wrote the program in java not knowing it needed to be in python, in order for this program to be integrated in with the OpenDSA backend, it had to be in python.   

*jsontrace.txt* is the sample input file for jsonFilter.py 

*filteredJSON.js* is the sample output file for the jsonFilter.py


jsonFilter.java
===============

The SampleBackEndTrace.txt contains an example of what the trace input (created from InMemory.java from the traceprinter package) would look like for the 
jsonFilter. 

The SampleFilteredTrace.js is what the ouput looks like after SampleBackEndTrace.txt has been passed 
through the jsonFilter. The ExecutionVisualizer functionality is from Philip Guo's Online Python Tutor (https://github.com/pgbovine/OnlinePythonTutor). 

jsonFilter.java reads in the backEndTrace as a string and removes unwanted execution points and outputs the javaScript 
file that is used by the HTML file to display the visualization of the generated trace. Two steps in one hopefully!
Time will tell... 
