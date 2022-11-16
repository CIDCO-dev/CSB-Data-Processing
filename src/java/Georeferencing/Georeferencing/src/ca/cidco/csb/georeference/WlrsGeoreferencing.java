package ca.cidco.csb.georeference;

import ca.cidco.csb.surveydata.Attitude;
import ca.cidco.csb.surveydata.Depth;
import ca.cidco.csb.surveydata.Position;

public class WlrsGeoreferencing extends Georeference{
	
	

	@Override
	protected BathymetryPoint georeference(Position position, Attitude attitude, Depth depth) throws Exception {
		throw new Exception("WLRS georeferencing not implemented");
	}

}
