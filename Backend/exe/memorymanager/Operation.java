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
 *  The root of the hierarchy of pointer operations
 *
 */

public abstract class Operation
{
    // location in source source code
    protected int lineNumber;
    protected int startHighlighting, stopHighlighting;
    //for second exp in compound bool exp of if, while, and for
    protected int startHighlighting2, stopHighlighting2; 

    // layout directives
    protected int row, col;
    protected String ref;

    public abstract void execute( GAIGSMemoryManager mm ) throws IOException;

    public void setLineNumber(int n)
    {
	lineNumber = n;
    }//setLinenumber method


    public int getLineNumber()
    {
	return lineNumber;
    }//getLinenumber method

    public void setStartHighlighting(int n)
    {
	startHighlighting = n;
    }//setStartHighlighting method

    public int getStartHighlighting()
    {
	return startHighlighting;
    }//getStartHighlighting method


    public void setStopHighlighting(int n)
    {
	stopHighlighting = n;
    }//setStopHighlighting method

    public int getStopHighlighting()
    {
	return stopHighlighting;
    }//getStopHighlighting method

    public void setStartHighlighting2(int n)
    {
	startHighlighting2 = n;
    }//setStartHighlighting2 method

    public void setStopHighlighting2(int n)
    {
	stopHighlighting2 = n;
    }//setStopHighlighting2 method

    public int getStartHighlighting2()
    {
	return startHighlighting2;
    }//getStartHighlighting2 method

    public int getStopHighlighting2()
    {
	return stopHighlighting2;
    }//getStopHighlighting2 method

}// Operation class