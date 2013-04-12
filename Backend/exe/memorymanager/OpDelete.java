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
 *   LHS is a non-null PointerExpression and RHS is a PointerExpression
 */

public class OpDelete extends Operation
{
    protected PointerExpression p; 

    /**
     * Creates an assignment operation after making sure that the LHS is not
     * a NULL pointer expression.
     *
     * @param    LHS       Left-hand side of the assignment.
     * @param    RHS       Right-hand side of the assignment.
     */
    public OpDelete( PointerExpression pexpr )
    {
	p = pexpr;
    }//constructor

    /**
     * Executes the assignment operation
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {	
	mm.setLineNumber( this.getLineNumber() );
	mm.delete( mm.getAddress( p ) ); 

    }//execute method
}// OpAssign class