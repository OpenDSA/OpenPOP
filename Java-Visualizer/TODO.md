TODO LIST
=========

JsonFilter
***
* Update the jsonFilter with functionality to remove the main function and all of its encoded variables from the "stack_to_render" section of each execution point.

* Write the JsonFilter in Python!!! So that the program can be integrated into the OpenDSA backend system. 


Visualizations
*** 
* Find a way to change the font color of the students code that is going to be visualized. It needs to be seperated from the code provided by the assignment. Example: 

        Link p = createList(1,2,3); //Code given to student by developer 
        Link r = p.next().next();  //Code given to student by developer

        p = p.next(); //Student Code that needs different font color

* Look into determining if the visualizer is capable of semantic analysis. Is it possible to change the way the visualization is presented to the student based on the objects they are instantiating or manipulating? Example: 

	-- Student manipulating a linked list. The Visualization should present the links in a horizontal order resembling the presentation style of the exercises jhave.org/JhavePOP. Whereas, if a student is finding values in a tree. The visualization should be presented in a way that better displays the data structure for understanding. 