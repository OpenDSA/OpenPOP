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
 * An IF-THEN-ELSE statement
 */

public class OpIf  extends Operation
{
    private BooleanExpression boolExpr;

    // statements making the body of the while loop
    private Operation thenB[];
    private Operation elseB[];
    private int numOps;

    public OpIf( BooleanExpression b )
    {
	this.boolExpr = b;
	this.thenB = null;
	this.elseB = null;
    }// constructor

    public void setThenBlock( Operation block[] )
    {
	thenB = block;
    }//setThenBlock method

    public void setElseBlock( Operation block[] )
    {
	elseB = block;
    }//setThenBlock method

    public void execute( GAIGSMemoryManager mm ) throws IOException
    {
        boolean value = mm.eval( boolExpr,  lineNumber );

	if ( value )
	{
	    for(int op=0; op < thenB.length; op++)
		if (thenB[op] != null)
		    thenB[op].execute( mm );

	}
	else if (elseB!=null)
	{
	    for(int op=0; op < elseB.length; op++)
		if (elseB[op] != null)
		    elseB[op].execute( mm );

	}

    }//execute method
}// OpIf class