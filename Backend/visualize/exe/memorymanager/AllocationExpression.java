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
 *  An allocation expression of the form:
 *      new Node( '<char>', <pointer expression> )
 */

public class AllocationExpression
{
    // the character in the info field (must be exactly one character)
    private Character info;          

    // the value where to find the info
    private PointerExpression infoPointer;

    // the value of the next pointer field
    private PointerExpression next;

    /**
     * Creates an allocation expression.
     *
     * @param    info      Info to be stored in the new node.
     * @param    next      Pointer to be stored in the next field.
     */
    public AllocationExpression(Character info, PointerExpression next)
    {
	this.info = info;
	this.next = next;
	infoPointer = null;
    }// 2-parameter constructor


    public AllocationExpression(PointerExpression info, PointerExpression next)
    {
	this.info = null;
	this.next = next;
	infoPointer = info;
    }// 2-parameter constructor


    /**
     * Returns the value of the info field.
     */
    Character getInfo()
    {
	return info;
    }//getInfo method


    /**
     * Returns the value of the info field.
     */
    PointerExpression getInfoPointer()
    {
	return infoPointer;
    }//getInfo method


    /**
     * Returns the value of the next field
     */
    PointerExpression getNext()
    {
	return next;
    }//getNext method

}// AllocationExpression class