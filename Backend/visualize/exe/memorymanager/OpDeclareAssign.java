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
 * A declaration operation of the form: 
 *                 Node *<id> = <id1>(->next)*;
 *              or Node *<id> = NULL;
 */

public class OpDeclareAssign  extends OpDeclare
{

    // <id> is inherited from OpDeclare

    // the pointer expression on the RHS
    private PointerExpression RHS; 

    /**
     * Creates a declare-and-assign operation.
     *
     * @param    id        The name of the pointer variable to be declared.
     * @param    RHS       The pointer expression to be assigned to it.
     */
    public OpDeclareAssign( String id, PointerExpression RHS,
			    int row, int col, String ref, String position)
    {
	super( id, row, col, ref, position );
	this.RHS = RHS;
    }// constructor

    /**
     * Returns the RHS of the operation.
     */
    PointerExpression getRHS()
    {
	return RHS;
    }//getPointerName method

    /**
     * Executes the declare-assign operation
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {
	mm.setLineNumber( this.getLineNumber() );

	mm.declareAndAssign ( id, RHS, row, col, ref, labelPosition); 

    }//execute method
}// OpDeclare class