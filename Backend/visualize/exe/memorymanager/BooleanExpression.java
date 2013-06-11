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

public class BooleanExpression
{
    protected String type;

    // left- and right-hand sides of the boolean expression
    // for pointer comparisons
    protected PointerExpression LHSp;
    protected PointerExpression RHSp;

    // left- and right-hand sides of the boolean expression
    // for info field comparison
    protected DataExpression LHSd;
    protected DataExpression RHSd;

    protected String comparator; // ==, !=, >, etc.


    protected int startHighlighting, stopHighlighting;
    protected int startHighlighting2, stopHighlighting2;

    public BooleanExpression() {};

    public BooleanExpression( String type,
			      PointerExpression LHS, PointerExpression RHS,
			      String comparator )
    {
        this.type = type;
	this.LHSp = LHS;
	this.RHSp = RHS;
	this.LHSd = null;
	this.RHSd = null;
	this.comparator = comparator;
        startHighlighting = -1;        
        stopHighlighting = -1;
    }// constructor

    public BooleanExpression( String type, 
			      DataExpression LHS, DataExpression RHS,
			      String comparator )
    {
        this.type = type;
	this.LHSp = null;
	this.RHSp = null;
	this.LHSd = LHS;
	this.RHSd = RHS;
	this.comparator = comparator;
        startHighlighting = -1;        
        stopHighlighting = -1;
    }// constructor

    public String getType()
    {
	return type;
    }//getType method


    public DataExpression getLHSd()
    {
	return LHSd;
    }//getLHSd method

    public PointerExpression getLHSp()
    {
	return LHSp;
    }//getLHSp method


    public DataExpression getRHSd()
    {
	return RHSd;
    }//getLHSd method


    public PointerExpression getRHSp()
    {
	return RHSp;
    }//getLHSp method

    public String getComparator()
    {
	return comparator;
    }//getComparator method

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

    public int getStartHighlighting2()
    {
	return startHighlighting2;
    }//getStartHighlighting2 method


    public void setStopHighlighting2(int n)
    {
	stopHighlighting2 = n;
    }//setStopHighlighting2 method

    public int getStopHighlighting2()
    {
	return stopHighlighting2;
    }//getStopHighlighting2 method

    public String toString(String derefStr, String nullStr, String infoStr)
    {
        String result;

        if (type.equals( "pointer" ))
            return 
		LHSp.toString(derefStr,nullStr) +  " " +
		comparator + " " +
		RHSp.toString(derefStr,nullStr);

	else
            return 
		LHSd.toString(derefStr,infoStr) +  " " +
		comparator + " " +
		RHSd.toString(derefStr,infoStr);

    }//toString method
}// BooleanExpression class