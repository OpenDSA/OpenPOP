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

import exe.*;

/**
 *  A layout directive, such as a suggested grid position for a new pointer
 *
 */

public class LayoutDirective
{
    private String type;
    private int row, col;
    private String ref, position;

    LayoutDirective( String type, 
		     int row, int col, String ref, String position)
    {
	this.type = type;
	this.row = row;
	this.col = col;
	this.ref = ref;
	this.position = position;
    }//constructor

    public String getType()
    {
	return type;
    }//getType method

    public int getRow()
    {
	return row;
    }//getRow method

    public int getCol()
    {
	return col;
    }//getCol method

    public String getRef()
    {
	return ref;
    }//getRef method

    public String getPosition()
    {
	return position;
    }//getPosition method

}//LayoutDirective class