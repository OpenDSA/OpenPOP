To install the module on local machine you will need the following resources 
 1) Jhava Jail files- You can download it from here https://github.com/daveagp/java_jail. 
    The README here https://github.com/daveagp/java_jail gives a detailed instruction of installation.
    
	These steps are needed :
	a) Download the repository and extract the files. 
		The folder structure is cp  dev  etc java lib64
                The java folder needs to have the jre and sdk installed for the InMemory.java file to be able to compile the class files and produce trace.
		You can find the Java distribution here - http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html.
		In my set up I used jdk-7u21-linux-x64.gz.
	b) Move to the folder cp.
		cd cp
	c) Run the Makefile.
		./Makefile
		This created the libraries needed and creates teh class files of major java files that producw the trace. The main class of interest is InMemory.java, in case you want to tweak some implementations.
Note all the jars required comes with the download , but I additionally required to download javax.json-1.0.4.jar.  

Once compiled, folder traceprinter has all the tracing java files.

2) Python tutor files- You can download the Puthon Tutor here https://github.com/pgbovine/OnlinePythonTutor/tree/master/v3
	The README here gives detailed explaination of the https://github.com/pgbovine/OnlinePythonTutor/blob/master/README of the code structure of PythonTutor. It majorly consisted of three two the front end visual manipulation using java scripts. and backend trace generation and file handling which they use different debugger for different languages. For java they used Jhava jail.
         
        THe major files to focus on are pytutor.js, pytutor-customization.css. 

3) JSAV - The visuals given by pytutor.js are direct mapping of heap and stack in the form of tables which were different from OpenDSA requirements. So I used the JSAV api which currently supports most of visulaizations. I Mainly worked with the JSAV.css files to assign classes to the generated data structure tables which modified the outputs.



