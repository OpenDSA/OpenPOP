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
 * A boolean expression
 */

public class CompoundBooleanExpression extends BooleanExpression
{
    boolean AND;

    BooleanExpression second;

    private int startHighlighting, stopHighlighting;

    public CompoundBooleanExpression( BooleanExpression e1, 
				      BooleanExpression e2,
				      boolean AND)
    {
        this.second = e2;
	this.AND = AND;
        if (e1.type.equals("pointer"))
	{
	    this.LHSp = e1.LHSp;
	    this.RHSp = e1.RHSp;
	    this.LHSd = null;
	    this.RHSd = null;
	}
	else
	{
	    this.LHSp = null;
	    this.RHSp = null;
	    this.LHSd = e1.LHSd;
	    this.RHSd = e1.RHSd;
	}
	this.type = e1.type;
	this.comparator = e1.comparator;
	startHighlighting = -1;        
	stopHighlighting = -1;
    }// constructor
    
    public BooleanExpression getSecond()
    {
	return second;
    }//getSecond method

    public String  getConnector()
    {
	if (AND) 
	    return "&&";
	else 
	    return "||";
    }//getConnector method


}// CompoundBooleanExpression class