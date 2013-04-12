/* 
This file is part of JHAVE -- Java Hosted Algorithm Visualization
Environment, developed by Tom Naps, David Furcy (both of the
University of Wisconsin - Oshkosh), Myles McNally (Alma College), and
numerous other contributors who are listed at the http://jhave.org
site

JHAVE is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

JHAVE is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with the JHAVE. If not, see:
<http://www.gnu.org/licenses/>.
*/

package exe.memorymanager;

import java.io.*;
import exe.*;

import java.io.FileReader;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.io.IOException;
import java.util.*;

public class memorymanager
{
    public static void main(String[] args) throws IOException
    {

	String showfilename = args[0] + ".sho";
	String pseudofilename = args[0] + ".php";
	String xmlstring = args[2];
	
	ShowFile show  = new ShowFile( showfilename );

	try
	{
	    Hashtable hash = XMLParameterParser.parseToHash( xmlstring );
	    String label = "Enter your Java or C++ source code below:";

	    String source = (String) hash.get( label );

	    Operation  program[] = null;
	    Parser parser;

	    PrintWriter phpWriter = createPHPfile( pseudofilename );

	    parser = new Parser( new StringBufferInputStream( source ) );


	    try {
		program = parser.parseProgram( phpWriter );
	    }	    
            catch (TokenMgrError e)
	    {
		// never reached so far
   	        show.writeSnap(e.toString(), 0.05,"", "");
		show.close();

		System.exit(0);
	    }

            catch (ParseException e)
	    {
   	        show.writeSnap(e.toString(), 0.05,"", "");
		show.close();

		System.exit(0);
	    }

	    System.out.print( "Creating php file...  ");
	    System.out.flush();
	    closePHPfile( phpWriter );

	    System.out.println( "done");


	    System.out.print( "Creating showfile... ");
	    System.out.flush();



	    GAIGSMemoryManager mm = 
		new GAIGSMemoryManager( parser.numRows, parser.numCols,
					0,0,parser.hSpacing,
					show, pseudofilename );

	    if (parser.drawgrid)
		mm.setDebugMode( true );

	    if (parser.listElements != null)
		mm.createLinkedList( parser.listHead, parser.listElements, 
				     parser.listTail );


	    for(int i=1; i<program.length; i++)
	    {
		if (program[i] != null)
		{
		    //System.out.println( i + " " + program[i].getLineNumber() + 
		    //	" " + program[i]);
		    if (program[i] instanceof OpWhile)
		    {
			//System.out.println( ((OpWhile)program[i]).getNumOps());
			//for(int j=0; j<((OpWhile)program[i]).getNumOps(); j++)
			    //System.out.println( "  " + ((OpWhile)program[i]).getOperation(j).getLineNumber() + " " +
			    //			((OpWhile)program[i]).getOperation(j));
		    }
		    //System.out.println( "start " + program[i] );

		    program[i].execute( mm );

		    //System.out.println( "done " );
		}
	    }
	}
	catch ( MemoryManagerException e)
	{
	    show.writeSnap(e.toString(), 0.05,"", "");
	}
	catch ( BreakException e) {
	    System.out.println( "caught the break exception ");
	}
	finally
	{
	    show.close();

	    System.out.println( "done");
	};


    }




    public String loadProgram(String filename) 
	throws IOException 
    {
        BufferedReader inputStream = null;
	String program = "";
        try {
            inputStream = 
                new BufferedReader(new FileReader( filename ));

	    String line;
            while ((line = inputStream.readLine()) != null)
		program += line + "\n";
        } 
	finally { if (inputStream != null) inputStream.close(); }

	return program;

    }// readCode method    

    private static PrintWriter createPHPfile( String pseudofile )
    {

    	// create the php file for the pseudocode pane
	try {
	    PrintWriter writer = 
		new PrintWriter( new FileWriter( new File( pseudofile ) ) );

	    writer.write("<?php\n" + "$pgm = array(\n");

	    return writer;
	} catch (IOException  e)
	{
            throw new MemoryManagerException("Problem creating " + 
					     pseudofile );
	}
    }// createPHPfile method


    private static void closePHPfile( PrintWriter writer )
    {

	writer.write( "\n);\n");
	writer.write(
		     "for($i = 0; $i < count($pgm); $i++){\n" +
		     "if($i ==$line){\n" +
                     "  if ($start != \"\") {\n" +
                     "     $temp1 = substr($pgm[$i],0,$start);\n" +
                     "     $temp2 = substr($pgm[$i],$start,$end - $start);\n" +
                     "     $temp3 = substr($pgm[$i],$end);\n" +
                     "     print(\"$temp1\");\n" +
		     "     print(\"<font color = 'red'>$temp2</font>\");\n" +
                     "     print(\"$temp3<br>\");\n" +
                     "  } else {\n"+
		     "     print(\"<font color = 'red'>$pgm[$i]</font><br>\");\n" +
                     " }\n" +
		     "} else\n" +
		     "print(\"$pgm[$i]<br>\");\n" +
		     "}\n" +
		     "?>" );
	writer.close();


    }// closePHPfile method

    /*
    private void createPHPfile2( String pseudofile, String program[] )
    {

    	// create the php file for the pseudocode pane
	try {
	    PrintWriter writer = 
		new PrintWriter( new FileWriter( new File( pseudofile ) ) );

	    writer.write("<?php\n" + "$pgm = array(\n");

	    // title line
	    writer.write( "\"<b>&nbsp; " +  titleLine + "</b><br>\",\n" );
	    
	    // initial linked list
	    if ( listElements != null)
		writer.write( "\" 0  " +  linkedListLine + "</b>\",\n" );
 
	    // skip grid size line

	    int lineNumber = 1;
	    for(int i=2; i<program.length; i++)
		if (program[i] != null)
		{
		    String line = program[i];

		    // skip full comment line with keyword equal to
		    // ... (none for now)
		    if (line.trim().indexOf("//") == 0)
		    {
			String tokens[] = line.split("\\s+");
			if (tokens[1].equals("newlist"))
			{
			    continue; // do not include this line in pseudocode
			}
		    }

		    // use to remove end of line comments in pseudocode
		    if (line.trim().indexOf("//") > 0)
			line = line.substring(0,line.indexOf("//"));

		    Formatter f = new Formatter();
		    String lnString = f.format("%2d",lineNumber).toString();
		    writer.write(
				 "\"" + lnString + "  " + line + "\"" +
				 ( (i+1<program.length)&&(program[i+1]!=null) ?
				   "," : "")
				 + "\n"
				 );
		    lineNumber++;
		}
	    writer.write( ");\n");
	    writer.write(
			 "for($i = 0; $i < count($pgm); $i++){\n" +
			 "if($i ==$line){\n" +
			 "print(\"<font color = 'red'>$pgm[$i]</font><br>\");\n" +
			 "}\n" +
			 "else\n" +
			 "print(\"$pgm[$i]<br>\");\n" +
			 "}\n" +
			 "?>" );
	    writer.close();
	} catch (IOException  e)
	    { javax.swing.JOptionPane.showMessageDialog( null, "IO exception in Driver" );}
    }
    */
    public String encode()
    {
	String s =  this.toString().replaceAll(  " < ", " &lt; ");
	s = s.replaceAll( " <= ", " &lt;= ");
	s = s.replaceAll( " > ", " &gt; ");
	s = s.replaceAll( " >= ", " &gt;= ");

	return s;
    }
}// Driver class
