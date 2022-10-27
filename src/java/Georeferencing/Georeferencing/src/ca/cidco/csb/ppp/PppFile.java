package ca.cidco.csb.ppp;

import java.util.ArrayList;

import ca.cidco.csb.surveydata.Position;

public class PppFile {
	
	private ArrayList<Position> pppPos = new ArrayList<Position>() ;
	
	public PppFile() {
	}
	
    public ArrayList<Position> getPositions() {
		return pppPos;
	}

	@Override
	public String toString() {
    	String output="";
    	for (Position pppPosition : pppPos) {
			output += pppPosition.toString();
    	} 
    	return output;
    }
}