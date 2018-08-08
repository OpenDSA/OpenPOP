# OpenPOP server

OpenPOP is a server that is implemented using Ruby on Rails 5. The server has Some Models, RubyTraceFilter.rb, JsavWrapper.js and Visualizers Backend
## Models
Currently, OpenPOP contains 3 models.

1. Exercise Model: the exercise model contains an entry for every exercises created on the server. Each exercise stored as an Exercise_ID and Exercise_Code. Exercise_code is the complete code, helper functions, main class or function, imports (includes), for the problem in hand except the lines of code that students should write to solve the  This model receives the student code (Answer) and imped it inside the the exercise code it has. This code will be sent to RubyTraceFilter.rb and receives back the trace.
2. Answer Model: This model represents an answer for an exercise. The relation between the Answer Model and Exercise Model is one to many relation. Thus, for each exercise, we can have many answers.
3. Trace Model: This Model represent the refined execution trace for each answer. The fact that most of students answer are identical (since the variable names are predetermined) the server stores the trace. The benefit of saving the trace is that if the server got an answer that is identical of an answer stored for the same exercise, it immediately reply with the stored trace back to the caller server (CodeWorkout). This will save a lot of time than generating the trace from scratch. The relation between the Trace and Answer is one to one.

### Notes:
To view these models on the server side, you can go to the following link: SERVER_URL/exercises
Each exercise can be viewed, modified or deleted using the appropriate link near each exercise.
Viewing an exercise will lead the user to a new page that will display the exercise and all answers and the trace tied with each answer.
Users can create new answers and visualize them directly from the server without the need to use CodeWorkout to solve these exercises. (Need a small Fix)

## RubyTraceFilter.rb
RubyTraceFilter is the file that is responsible of receiving a complete source code and returns back the generated trace. The steps to achieve that trace are
This file receives the code from the Exercise Model through the main method.
The main method receives the full code and student_id. It uses the full code to generate the execution trace. After that, the trace will be filtered to remove all unnecessary parts from it. There are 2 main filters on the execution trace which are removing all traces that are not related to student lines of code, and remove all unnecessary data from trace lines resulting after the first filter.
### Removing all trace lines that are not related to student solution. 
The complete execution trace, that was generated from the complete source code, contains many line that are not related to the student solution. These lines of traces are removed. To do the, there are two functions calls that are marking the student code. The program serch on these 2 functions call and extract all trace lines in between. This way, the program filtered out all execution traces that are not related to student lines of code.

Every exercise code contains these two functions:
```
public static void endTraceNow(){}
public static void startTraceNow(){}
```
These two functions are empty functions and the main purpose for them is to mark the student code. Thus, the program will be able to extract the intended execution trace. Here is an example of the function that will hold the student solution to an exercise.
```
public static Link changeNext(Link p, Link r) 
{
    startTraceNow(); 
    __ 
    endTraceNow(); return p; } 
} 
```
The program will replace ```__``` with students lines of code to form a complete source code for the exercise.

### Removing unnessesary trace information
The generated execution trace holds a lot of inforamtion. OpenPOP does not use all of these data to visualize the code (It may requier some of them later when we expand the project). Therefore, the program filter out all these data that are not important in the current version. The main reason to this filtration is to reduce the amount of data transfered over the network between OpenPOP and the caller server (Currently, CodeWorkout). Here is an example for the trace before and after this filtreing process.
#### Before
```
Trace: {"stdout":"","event":"step_line","line":1,"stack_to_render":[{"func_name":"changeNext:1","encoded_locals":{"p":["REF",175],"r":["REF",173]},"ordered_varnames":["p","r"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"282","frame_id":282}],"globals":{},"ordered_globals":[],"func_name":"changeNext","heap":{"173":["INSTANCE","Link",["next",null],["data",3]],"175":["INSTANCE","Link",["next",["REF",174]],["data",1]],"174":["INSTANCE","Link",["next",["REF",173]],["data",2]]}}, {"stdout":"","event":"step_line","line":1,"stack_to_render":[{"func_name":"changeNext:1","encoded_locals":{"p":["REF",174],"r":["REF",173]},"ordered_varnames":["p","r"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"290","frame_id":290}],"globals":{},"ordered_globals":[],"func_name":"changeNext","heap":{"173":["INSTANCE","Link",["next",null],["data",3]],"174":["INSTANCE","Link",["next",["REF",173]],["data",2]],"175":["INSTANCE","Link",["next",["REF",174]],["data",1]]}} 
```
#### After
```
Trace: [{"stack":{"ordered_variable_names":["p","r"],"encoded_locals":{"p":["REF",182],"r":["REF",184]}},"heap":{"182":["INSTANCE","Link",["next",["REF",183]],["data",1]],"183":["INSTANCE","Link",["next",["REF",184]],["data",2]],"184":["INSTANCE","Link",["next",null],["data",3]]},"code":" p = p.next;","lineNumber":0},{"stack":{"ordered_variable_names":["p","r"],"encoded_locals":{"p":["REF",183],"r":["REF",184]}},"heap":{"183":["INSTANCE","Link",["next",["REF",184]],["data",2]],"184":["INSTANCE","Link",["next",null],["data",3]]},"code":"return statement","lineNumber":2}] 
```
By locking closely at these traces, there is a big difference in the length of them. Also, OpenPOP augmented the AFTER trace with some useful data like the line number of the code and the code line that generates this trace.

After the trace is filtered and retured back to the OpenPOP server, the server replies back to the caller with execution trace for the given source code.

## JsavWrapper.js
This file contains the code that used to visualize the student code. The main function in this file reads the trace, create the JSAV object that will be used to viusalize the trace, and creates the slides that show the student the execution steps for his/her lines of code.

## Visualizers Backend
There are tools that used to generate the execution traces. The current version of this server uses [Java_Jail](https://github.com/daveagp/java_jail) to generate execution traces for any source code wriiten in JAVA. In the future expansion, the server may use [opt-cpp-backend](https://github.com/pgbovine/opt-cpp-backend).
Both of these tools are used as back ends in [Python Tutor](http://pythontutor.com/) for Java and C++/C code.

# Setting Up a Vagrant Environment for OpenPOP
## Introduction:
Vagrant is designed to run on multiple platforms, including Mac OS X, Microsoft Windows, Debian, Ubuntu, CentOS, RedHat and Fedora. In this document we describe how to configure and run OpenPOP project virtual development environment through Vagrant.

## Installation Steps:
1) Install [Vagrant](https://www.vagrantup.com/downloads.html)
2) Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
3) ```Clone this repository```
4) ```$ cd OpenPOP```
5) ```$ vagrant up```
6) ```$ vagrant ssh```
7) ```$ . /vagrant/runservers.sh```
8) After the provisioning script is complete you can go to:
https://192.168.33.10:3000 for OpenPOP server

## Shut Down The Virtual Machine:
After you finish your work, you need to turn the virtual machine off.

1) Exit the virtual machine terminal by typing ```exit```
2) ```$ cd OpenPOP```
3) ```$ vagrant halt```

## Re-run Development Servers:
If you decided to shut down the virtual machine using vagrant halt, you have to re-run the servers again after you do vagrant up.

1) ```$ cd OpenPOP```
2) ```$ vagrant up```
3) ```$ vagrant ssh```
4) ```$ cd /vagrant```
5) ```$ rails server```

## Reprovision The Virtual Machine:
If anything went wrong or you want to reprovision your virtual machine for any reason, follow these steps.

1) ```$ cd OpenPOP```
2) ```$ git pull```
3) ```$ vagrant destroy```
4) ```$ vagrant up```

## Virtual Machine sudo password:
sudo password is vagrant in case you need to execute any commands that require sudo.

## Keep OpenPOP repository up to date:
During development of OpenPOP, other developers might add new gems to the project or add new migrations etc. To keep your local version up to date with the latest version do the following:

1) Open a new terminal
2) ```$ cd OpenPOP```
3) ```$ git pull```
4) ```$ vagrant reload```
5) ```$ vagrant ssh```
6) ```$ cd /vagrant```
7) ```$ sudo bundle install```
8) ```$ rake db:populate ``` Note: This step will place the database in a simple starter state.
9) ```$ . /vagrant/runservers.sh```