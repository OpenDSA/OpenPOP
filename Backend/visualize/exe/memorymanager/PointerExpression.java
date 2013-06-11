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
 *  A pointer expression may be of one of two types:
 *   1.   NULL
 *   2.   <id>(->next)* where <id> is the name of a pointer variable
 *
 */

public class PointerExpression
{
    // the name of the pointer variable
    // or "NULL" if the PointerExpression is of type 1
    private String id;          

    // the number of next pointer dereferences (0 and up)
    // or -1 if the PointerExpression is of type 1
    private int length;  

    /**
     * Creates a pointer expression of type 1
     */
    public PointerExpression()
    {
	id = "NULL";
	length = -1;
    }// default constructor


    /**
     * Creates a pointer expression of type 2
     *
     * @param    id        Name of the pointer variable.
     * @param    length    Number (>= 0) of next pointers to dereference.
     */
    public PointerExpression(String id, int length)
    {
	this.id = id;
	this.length = length;
    }// 2-parameter constructor


    /**
     * Returns the pointer variable at the head of the pointer expression.
     */
    public String getPointerName()
    {
	return id;
    }//getPointerName method


    /**
     * Returns the length of the chain of next pointers.
     */
    public int getChainLength()
    {
	return length;
    }//getChainLength method

    /**
     * Returns true iff the pointer expression is of type 1
     */
    public boolean isNull()
    {
	return ( id.equals("NULL") && (length==-1) );
    }//isNullMethod


    public String toString(String derefStr, String nullStr)
    {
        if (isNull())
            return nullStr;
        else
	{
	    String result = getPointerName();

	    for(int i=0; i<getChainLength(); i++)
		result += derefStr + "next";

            return result;
	}
    }//toString method

}// PointerExpression class