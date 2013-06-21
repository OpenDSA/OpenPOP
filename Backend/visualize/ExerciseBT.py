# Create your views here.

from django.http import HttpResponse
import xml.etree.ElementTree as xml # for xml parsing
import shlex # for strings splitting
import re # for special characters escaping
import os
import subprocess
import codecs
#from subprocess import call
#import pdb; pdb.set_trace()
def btassess(data):
    feedback=''
    filesPath = '/home/OpenPOP/Backend/visualize/build/TreeTest/javaSource/'
    print "In the begining of assessing the code using java compiler"
    #cleaning: deleting already created files
    if os.path.isfile(filesPath +'studentpreordertest.java'):
       os.remove(filesPath+'studentpreordertest.java')
 
    if os.path.isfile(filesPath +'output'):
       os.remove(filesPath+'output')

    if os.path.isfile(filesPath +'compilationerrors.out'):
       os.remove(filesPath + 'compilationerrors.out')
   
    if os.path.isfile(filesPath +'runerrors.out'):
       os.remove(filesPath + 'runerrors.out')

   
    # Saving the submitted/received code in the studentpreordertest.java file by copying the preorder + studentcode +}
    BTTestFile = open(filesPath+'PreorderTest.java' , 'r')
    BTtest = BTTestFile.read()
    answer = open(filesPath+'studentpreordertest.java', 'w')
    answer.write(BTtest)
    answer.write("public static")
    answer.write(data.decode('utf-8'))
    answer.write("}")
    answer.close()
    
    # Setting the DISPLAY then run the processing command to test the submitted code
    proc1 = subprocess.Popen(" cd /home/OpenPOP/Backend/visualize/build/TreeTest/javaSource/; javac studentpreordertest.java 2> /home/OpenPOP/Backend/visualize/build/TreeTest/javaSource/compilationerrors.out ; java studentpreordertest 2> /home/OpenPOP/Backend/visualize/build/TreeTest/javaSource/runerrors.out", stdout=subprocess.PIPE, shell=True)
    (out1, err1) = proc1.communicate() 
    
    print data
    # Read the success file if has Success inside then "Well Done!" Otherwise "Try Again!"
    if  os.path.isfile(filesPath+'compilationerrors.out'):
          syntaxErrorFile = open(filesPath+'compilationerrors.out' , 'r')
          feedback= syntaxErrorFile.readlines()
          syntaxErrorFile.close()
          if os.stat(filesPath+'compilationerrors.out')[6]!=0:
             return feedback;
    if os.path.isfile(filesPath+'runerrors.out'):
       #Check what is returned from the test : what is inside the success file
          runErrorFile = open(filesPath+'runerrors.out' , 'r')
          feedback= runErrorFile.readlines()
          runErrorFile.close()
          if os.stat(filesPath+'runerrors.out')[6]!=0:
             return feedback;
    
    
    if os.path.isfile(filesPath+'output'):
       #Check what is returned from the test : what is inside the success file
       successFile = open(filesPath+'output' , 'r')
       feedback = successFile.readlines() 
      
    return  feedback
