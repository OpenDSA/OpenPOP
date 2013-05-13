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
 * An assignment operation: LHS = RHS      where
 *   LHS is a non-null PointerExpression 
 *   and RHS is an AllocationExpression
 */

public class OpAssignAllocate extends OpAssign
{
    private AllocationExpression RHSnew; 

    /**
     * Creates an assignment operation after making sure that the LHS is not
     * a NULL pointer expression.
     *
     * @param    LHS       Left-hand side of the assignment.
     * @param    RHS       Right-hand side of the assignment.
     */
    public OpAssignAllocate( PointerExpression LHS, AllocationExpression RHS, int row, int col)
    {
	/*
	if (LHS.isNull())
	    throw ...

	*/
	super( LHS, null );
	this.RHSnew = RHS;
	this.row = row;
	this.col = col;
        startHighlighting = -1;        
	stopHighlighting = -1;
	
    }// 2-parameter constructor

    /**
     * Executes the assignment operation
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {

        String info;

	if (RHSnew.getInfo() != null)
	    info = RHSnew.getInfo().toString();
        else
	{
            PointerExpression pexpr = RHSnew.getInfoPointer();

	    /*
            Index index = getValue( getNext( getAddress( 
                                                  pexpr.getPointerName(),
                                                  pexpr.getChainLength)));
	    */
            info = mm.getInfo( pexpr );
        }
	mm.setLineNumber( this.getLineNumber() );
	mm.assign( 
		  mm.getAddress( LHS ),

		  ( RHSnew.getNext().isNull() ?
		    mm.allocateNode( info,
				     "null", -1, row, col) :
		    mm.allocateNode( info,
				     RHSnew.getNext().getPointerName(), 
				     RHSnew.getNext().getChainLength(),
				     row, col)
		    ),
		  startHighlighting, stopHighlighting
		  );
    }//execute method
}// OpAssignAllocate class