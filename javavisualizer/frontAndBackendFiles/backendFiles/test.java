import java.io.FileWriter;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.io.PrintWriter;

/* *** ODSATag: Link *** */
class Link {
  private Object e;
  private Link n;

  // Constructors
  Link(Object ine, Link inn) { e = ine; n = inn; }
  Link(Link inn) { e = null; n = inn; }

  public  Object element() { return e; }           // Return the value
  public void setelement(Object ine) { e = ine; } // Set element value
  public Link next() { return n; }                // Return next link
  public void setnext(Link inn) { n = inn; }      // Set next link
}
/* *** ODSAendTag: Link *** */

public class studentpntrequalspntrPROG {

public static void main(String [ ] args) {


boolean SUCCESS = false;

  Link studentsHead; 
  
  studentsHead = reAssignPointer(); 
  
  Link Mthird = new Link(3,null); 
  Link Msecond = new Link(2,Mthird); 
  Link Mfirst = new Link(1,Msecond); 
	
  Link Mp; 
  Link Mq; 
  Link Mr; 
	
  Mp = Mfirst;
  Mq = Msecond;
  
  Mp = Mq;  
  
  if (Mp.element() == studentsHead.element()) SUCCESS = true;

  try{

  
  PrintWriter output = new PrintWriter("output", "UTF-8");


   if (SUCCESS) { 
   
     output.println("Well Done!");
     output.close();
   }
   else 
   {
     output.println("Try Again! You have either disconnected your links or incorrectly reassigned the variable p.");
     output.close();
      
   }
   
  }
  catch (IOException e) {
	e.printStackTrace();
  }


}

public static Link createList(int one, int two, int three) { 
    
    Link tail = new Link(three,null); 
    Link next = new Link(two,tail); 
    Link head = new Link(one,next); 
    
    return head; 
}

public static void endTraceNow(){
    
    //End the trace 
    // This function's only purpose is to act as a flag to end the trace 
    // for the Java - Visualization 
}

public static void startTraceNow(){
    
    //start the trace 
    // This function's only purpose is to act as a flag to start the trace 
    // for the Java - Visualization 
}

public static boolean checkIfLinksLinked(Link head){
    
    Object two = 2; 
    Object three = 3; 
    
    boolean linkFlag = false; 
    
    if(head.element() == two) 
    {
        if(head.next().element() == three) 
        {
            linkFlag = true; 
        }
        else 
        {
            linkFlag = false; 
        }
    }
    else 
    {
        linkFlag = false; 
    }
    
    return linkFlag; 
}



public static Link reAssignPointer() {
	
	startTraceNow(); 

	Link p = createList(1,2,3); 
	Link q = p.next(); 

	p = q; 
	
	endTraceNow(); 

	return p; 

	}

}

