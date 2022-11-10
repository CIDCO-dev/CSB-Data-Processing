package ca.cidco.csb.georeference;

import java.util.ArrayList;

import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.RealVector;

import ca.cidco.csb.surveydata.Attitude;
import ca.cidco.csb.surveydata.Depth;
import ca.cidco.csb.surveydata.Position;
import ca.cidco.csb.utilities.Conversion;
import ca.cidco.csb.utilities.Geodesy;

public class ErsGeoreferencing extends Georeference{

	double leverArmX;
	double leverArmY;
	double leverArmZ;
	double draft;
	double a= Geodesy.a;
	double e= Geodesy.e;
	
	public ErsGeoreferencing(Job job) {
		leverArmX= job.getLeverArmX;
		leverArmY= job.getLeverArmY;
		leverArmZ= job.getLeverArmZ;
		draft= job.getDraft;
	}
	
	

	@Override
	protected BathymetryPoint georeference(Position position, Attitude attitude, Depth depth) {

		RealVector abi = new ArrayRealVector(new double[] { leverArmX, leverArmY, leverArmZ });
		
// Remove draft
//Zprofil = Zprofil.array() - draft;
		
		//Convert Euler angles to radians
		double roll = Conversion.deg2Rad(attitude.getRoll());
		double pitch =Conversion.deg2Rad(attitude.getPitch());
		double heading = Conversion.deg2Rad(attitude.getHeading());
		
		//Convert lat/lon to radians
		double lat = Conversion.deg2Rad(position.getLatitude());
		double lon = Conversion.deg2Rad(position.getLongitude());

//// Refraction correction
//double rn1, rn2, rn3;
//RayTracing(rn1, rn2, rn3, Roll, Pitch, Heading, TravelTime, Cprofil, Zprofil);

		//if (TypeSurvey == "ERS")
		//{
		//// Merging: CnTRF*(Pn + rn + Cbin*abi)
		//double xTRF, yTRF, zTRF;
		//merging(xTRF, yTRF, zTRF, rn1, rn2, rn3, lat, lon, height_Ell_WL, Roll, Pitch, Heading, abi, a, e);
		//
		//// Soundings' geographic coordinates
		//ECEF_2_LatLonH(latGeoref, lonGeoref, hGeoref, xTRF, yTRF, zTRF, a, e);
		//}
		//

//
//// Transform to degres: We add HeightWL to h
		double latGeoref = Conversion.rad2Deg(latGeoref);
		double lonGeoref = Conversion.rad2Deg(lonGeoref);
		
		
		
		
		
		BathymetryPoint bathymetryPoint= new BathymetryPoint(depth.getTimestamp(), lonGeoref, latGeoref, hGeoref, position.getSdLongitude(), position.getSdLatitude(), position.getSdHeight());
		
		return bathymetryPoint;
	}

}
