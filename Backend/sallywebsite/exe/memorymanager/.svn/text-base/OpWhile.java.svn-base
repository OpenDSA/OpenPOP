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
 * A while command
 */

public class OpWhile  extends Operation
{
    BooleanExpression b;

    // statements making up the body of the while loop
    private Operation[] body;
    private int numOps;

    public OpWhile( BooleanExpression b )
    {
	this.b = b;
	this.numOps = 0;
	this.body = new Operation[ 100 ];
    }// constructor

    public int getNumOps()
    {
	return numOps;
    }//getNumOps method


    public Operation getOperation( int i )
    {
	if ( i > numOps )
	    return new OpNone();
	else
	    return body[i];
    }//getOperation method

    public void addOperation( Operation op )
    {
	if ( numOps == 100 )
	    return;
	else
	    body[ numOps++ ] = op;
    }//addOperation method

    /**
     * Executes the while command
     */
    public void execute( GAIGSMemoryManager mm ) throws IOException
    {
	int kill_count = 0;
	while ( mm.eval( b, lineNumber ) )
	{
	    kill_count++;
	    if (kill_count > 20) throw new MemoryManagerException("Loop limit of 20 reached");
	    try {
		for(int op=0; op < numOps; op++)
		    body[op].execute( mm );
	    } catch( BreakException e )  {    
		break; 
	    }
	}

    }//execute method
}// OpWhile class