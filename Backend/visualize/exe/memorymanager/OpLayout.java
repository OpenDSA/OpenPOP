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

/**
 * An hint for the layout manager
 */

public class OpLayout extends Operation
{
    private String type;
    private String pointerName;
    private int row, col, ref;

    /**
     */
    public OpLayout()
    {
        type = "";
	pointerName = "";
	row = col = ref = 0;
    }// default constructor


    public OpLayout( String type, String pointerName )
    {
        this.type = type;
	this.pointerName = pointerName;
	row = col = ref = 0;
    }// constructor

    /**
     * Returns the 
     */
    String getType()
    {
	return type;
    }//getType method

    /**
     * Executes the layout operation
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {
	mm.setLineNumber( this.getLineNumber() );
	if (type.equals( "redraw" ))
	    mm.redrawLinkedList( mm.getAddress( pointerName ) );

    }//execute method
}// OpLayout class