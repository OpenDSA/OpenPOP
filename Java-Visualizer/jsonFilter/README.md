jsonFilter.py
=============
This is a Python version of the jsonFilter.java, except the jsonFilter.py contains different functionality and is much closer to a complete program. jsonFilter.py has capabilities to read in a .java file and produce filtered execution traces that were specified by the OpenDSA backend developer. 

This file does 3 things: 

1. Reads in the backend j-unit test file 

2. Generates a json trace from the entire j-unit test file. This trace is a string that consists of over 60,000 characters in the case of the normal j-unit test from OpenDSA exercises. 

3. Filters the backend json trace down to about 2,000 characters and outputs the results into a formatted JavaScript file. TODO: This file format may not be transferable from the backend to the frontend in the existing OpenDSA infrastructure. Rather then printing out to a file, place the contents into a string that can be retrieved programmatically by frontend.  

This program was developed to isolate certain lines of code to be visualized by the Java version of Philip Guo's Online Python Tutor. This file utilizes the traceprinter package from David Pritchard's repository https://github.com/daveagp/java_jail/tree/master/cp to run the shell command to produce the backend json trace. The backend json trace is a string consisting of over 10,000 characters (in most cases) that is used to visualize java code. The jsonFilter.py locates the execution points that are specified using the startTraceNow() and endTraceNow() functions, which are dummy functions inserted into the j-unit test in the OpenDSA backend that wrap the code presented to the student and the student's code, both intended for visualization.   


jsonFilter.java
===============

The SampleBackEndTrace.txt contains an example of what the trace input (created from InMemory.java from the traceprinter package) would look like for the 
jsonFilter. 

The SampleFilteredTrace.js is what the ouput looks like after SampleBackEndTrace.txt has been passed 
through the jsonFilter. The ExecutionVisualizer functionality is from Philip Guo's Online Python Tutor (https://github.com/pgbovine/OnlinePythonTutor). 

jsonFilter.java reads in the backEndTrace as a string and removes unwanted execution points and outputs the javaScript 
file that is used by the HTML file to display the visualization of the generated trace. Two steps in one hopefully!
Time will tell... 
