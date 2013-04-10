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
 *                 Node *<id> = <allocation expression>
 */

public class OpDeclareAllocateAssign  extends OpDeclare
{

    // <id> is inherited from OpDeclare

    // the allocation expression on the RHS
    private AllocationExpression RHS; 

    /**
     * Creates a declare-allocate-and-assign operation.
     *
     * @param    id        The name of the pointer variable to be declared.
     * @param    RHS       The allocation expression.
     */
    public OpDeclareAllocateAssign( String id, AllocationExpression RHS,
				    int row, int col, String ref, 
				    String position)
    {
	super( id, row, col, ref, position );
	this.RHS = RHS;
	
    }// constructor

    /**
     * Returns the RHS of the operation.
     */
    AllocationExpression getRHS()
    {
	return RHS;
    }//getRHS method

    /**
     * Executes the declare-allocate-assign operation
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {
	mm.setLineNumber( this.getLineNumber() );

        String info;

	if (RHS.getInfo() != null)
	    info = RHS.getInfo().toString();
        else
	{
            PointerExpression pexpr = RHS.getInfoPointer();
            info = mm.getInfo( pexpr );
        }

	mm.declareAllocateAndAssign( id,
				     info,
				     RHS.getNext(),
				     labelPosition,
				     row, col, ref);
    }//execute method
}// OpDeclareAllocateAssign class