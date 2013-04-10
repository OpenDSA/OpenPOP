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
 * A data expression of the form 'X' or <p><chain>.info
 */

public class DataExpression
{
    private PointerExpression pexpr;
    private String character;

    public DataExpression( PointerExpression pexpr )
    {
	this.pexpr = pexpr;
	this.character = "";
    }// constructor

    public DataExpression( String character )
    {
	this.pexpr = null;
	this.character = character;
    }// constructor

    public String getCharacter()
    {
	return character;
    }//getCharacter method


    public PointerExpression getPointerExpression()
    {
	return pexpr;
    }//getPointerExpression method

    public String toString(String derefStr, String infoStr)
    {
        if (!character.equals(""))
            return "'" + character + "'";
        else
	{
            String result = pexpr.getPointerName();
            for(int i=0; i<pexpr.getChainLength(); i++)
                result += derefStr + "next";
            result += derefStr + infoStr;
            return result;
        }


    }//toString method
}// DataExpression class