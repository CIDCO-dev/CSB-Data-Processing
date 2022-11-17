package ca.cidco.csb.surveyplatform;

import java.util.ArrayList;

import ca.cidco.csb.surveydata.Attitude;
import ca.cidco.csb.surveydata.Depth;
import ca.cidco.csb.surveydata.Position;

public interface SurveyPlatform {
	public ArrayList<Position> getPositions();
	public void setPositions(ArrayList<Position> p);
	
	public ArrayList<Attitude> getAttitudes();
	public ArrayList<Depth> getDepths();
	
}
