# Create your views here.

from django.http import HttpResponse
import xml.etree.ElementTree as xml # for xml parsing
import shlex # for strings splitting
import re # for special characters escaping
import os
import subprocess
#from subprocess import call
#import pdb; pdb.set_trace()
def assess_code(data):
    feedback=''
    print "I am in the begining of assessing the code"
    #cleaning: deleting already created files
    if os.path.isfile('/home/OpenPOP/Backend/visualize/build/ListTest/output'):
       os.remove('/home/OpenPOP/Backend/visualize/build/ListTest/output')

    if os.path.isfile('/home/OpenPOP/Backend/visualize/build/ListTest/studentAnswer.pde'):
       os.remove('/home/OpenPOP/Backend/visualize/build/ListTest/studentAnswer.pde')

    if os.path.isfile('/home/OpenPOP/Backend/visualize/build/ListTest/serr.out'):
       os.remove('/home/OpenPOP/Backend/visualize/build/ListTest/serr.out')

    # Saving the submitted/received code in the studentAnswer.pde file
    answer = open('/home/OpenPOP/Backend/visualize/build/ListTest/studentAnswer.pde', 'w')
    answer.write(data)
    answer.close()
    
    # Setting the DISPLAY then run the processing command to test the submitted code
    proc = subprocess.Popen("export DISPLAY=':2';/home/processing-2.0b9/processing-java --run --sketch='/home/OpenPOP/Backend/visualize/build/ListTest' --output='/home/OpenPOP/Backend/visualize/build/build' --force 2> /home/OpenPOP/Backend/visualize/build/ListTest/serr.out", stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print data
    # Read the success file if has Success inside then "Well Done!" Otherwise "Try Again!"
    if os.path.isfile('/home/OpenPOP/Backend/visualize/build/ListTest/output'):
       #Check what is returned from the test : what is inside the success file
       successFile = open('/home/OpenPOP/Backend/visualize/build/ListTest/output' , 'r')
       feedback = successFile.readlines()
      
    else :
       if os.path.isfile('/home/OpenPOP/Backend/visualize/build/ListTest/serr.out'):
       #Check what is returned from the test : what is inside the success file
          syntaxErrorFile = open('/home/OpenPOP/Backend/visualize/build/ListTest/serr.out' , 'r')
          feedback= syntaxErrorFile.readlines()
    
    return  feedback
