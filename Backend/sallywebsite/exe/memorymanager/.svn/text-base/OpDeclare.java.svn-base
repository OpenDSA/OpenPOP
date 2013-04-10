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
 * A declaration operation: Node *<id>;
 */

public class OpDeclare  extends Operation
{
    // the name of the pointer variable
    protected String id;   
    protected String labelPosition;

    /**
     * Creates a declaration operation
     *
     * @param    id        Name of the pointer variable.
     */
    public OpDeclare( String id )
    {
	this.id = id;
	this.labelPosition = "";
    }// constructor


    public OpDeclare( String id, int row, int col, String ref )
    {
	this.id = id;
	this.row = row;
	this.col = col;
	this.ref = ref;
	this.labelPosition = "";
    }// constructor


    public OpDeclare( String id, int row, int col, String ref, String position)
    {
	this.id = id;
	this.row = row;
	this.col = col;
	this.ref = ref;
	this.labelPosition = position;
    }// constructor

    /**
     * Returns the name of the pointer variable.
     */
    String getPointerName()
    {
	return id;
    }//getPointerName method

    /**
     * Executes the assignment operation
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {
	mm.setLineNumber( this.getLineNumber() );
	mm.declare( id, labelPosition, row, col, ref );
    }//execute method
}// OpDeclare class