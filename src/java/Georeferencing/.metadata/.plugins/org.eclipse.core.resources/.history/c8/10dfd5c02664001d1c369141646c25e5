package ca.cidco.csb;


import java.util.Vector;
import java.lang.Math;
//import ca.cidco.csb.MatrixXd;


public class Georeferencing {
	
	final static double PI = 3.14159265358979323846;
	double x;
	double y;
	double z;
	MatrixXd Cbin_NED = new MatrixXd();
	
	
	public Georeferencing() {
		// TODO Auto-generated constructor stub
	}
	
	// DCM: C_bi_n - NED convention

	/**
	 * Compute the Direction Cosine Matrix
	 * 
	 * @param Cbin_NED The Direction Cosine Matrix
	 * @param Roll the roll angle of the boat in degrees w.r.t the navigation frame
	 * @param Pitch the angle value of the pitch movement of the boat (degrees)
	 * @param Heading the angle value of the yaw movement of the boat (degrees)
	 */
	public void dcm(double Roll, double Pitch, double Heading) {
		
		// Initialisation
		double cR = Math.cos(Roll);
		double sR = Math.sin(Roll);
		
		double cP = Math.cos(Pitch);
		double sP = Math.sin(Pitch);
		
		double cY = Math.cos(Heading);
		double sY = Math.sin(Heading);

		// DCM                                
		Cbin_NED.initializeMatrixXd(cR, sR, cP, sP, cY, sY);
//		Cbin_NED.printMatrix(Cbin_NED);
		

	}
	

//	
//	
//    
//	/**
//     * Procède au géoréférencement d'un point de sonde.
//     *
//     * @param latGeoref Coordonnée géographique de latitude du point de sonde géoréréfencé  (degrés)
//     * @param lonGeoref Coordonnée géographique de longitude du point de sonde géoréréfencé (degrés)
//     * @param hGeoref Coordonnée d'élévation du point de sonde géoréréfencé (mètres)
//     * @param TypeSurvey  Type de méthode de réduction: 'Water Level Reduced soundings' (WLRS) ou 'Ellipsoidal Reduced Soundins' (ERS)
//     * @param a Demi grand axe de l'ellipsoide de reference
//     * @param e Première excentricité de l'ellipsoide de reference
//     * @param leverArmX Composante N   du bras de levier (m)
//     * @param leverArmY Composante E du bras de levier (m)
//     * @param leverArmZ Composante D du bras de levier (m)
//     * @param draft Draft
//     * @param TravelTime ONE WAY temps de parcours de la sonde acoustique en (s)
//     * @param Roll  roulis en rad
//     * @param Pitch  tangage en rad
//     * @param Heading  cap en radian
//     * @param lat   latitude en degré
//     * @param lon  longitude en degré
//     * @param height_Ell_WL Hauteur par rapport à l'ellipsoide ou au niveau d'eau, selon la méthode de reduction des sondes
//     */
//	
// 	Georeferencing(	double latGeoref, double lonGeoref, double hGeoref, String TypeSurvey, double a, double e,
//    									double leverArmX,double leverArmY, double leverArmZ, double draft, double TravelTime,
//    									double Roll, double Pitch, double Heading, double lat, double lon, double height_Ell_WL) {
//    	// Lever arms
//    	Vector<Double> abi = new Vector<Double>();
//    	abi.add(leverArmX);
//    	abi.add(leverArmY);
//    	abi.add(leverArmZ);
//    	
//    	// Remove draft
////    	Zprofil = Zprofil.array() - draft;
//
//    	//Convert Euler angles to radians
//    	Roll = (Roll * PI)/180;
//    	Pitch = (Pitch * PI)/180;
//    	Heading = (Heading * PI)/180;
//
//    	//Convert lat/lon to radians
//    	lat = (lat *PI)/180;
//    	lon = (lon *PI)/180;
//
//    	// Refraction correction
//    	double rn1, rn2, rn3;
//    	RayTracing(rn1, rn2, rn3, Roll, Pitch, Heading, TravelTime, Cprofil, Zprofil);
//
//    	if (TypeSurvey == "ERS")
//    	{
//    		// Merging: CnTRF*(Pn + rn + Cbin*abi)
//    		double xTRF, yTRF, zTRF;
//    		merging(xTRF, yTRF, zTRF, rn1, rn2, rn3, lat, lon, height_Ell_WL, Roll, Pitch, Heading, abi, a, e);
//
//    		// Soundings' geographic coordinates
//    		ECEF_2_LatLonH(latGeoref, lonGeoref, hGeoref, xTRF, yTRF, zTRF, a, e);
//    	}
//
//    	// WLRS survey: (latitude, longitude, 0) is converted to TRF
//    	else
//    	{
//    		// Merging: CnTRF*(Pn + rn + Cbin*abi)
//    		double xTRF, yTRF, zTRF;
//    		merging(xTRF, yTRF, zTRF, rn1, rn2, rn3, lat, lon, 0, Roll, Pitch, Heading, abi, a, e);
//
//    		// Soundings' geographic coordinates
//    		ECEF_2_LatLonH(latGeoref, lonGeoref, hGeoref, xTRF, yTRF, zTRF, a, e);
//
//    		// Height wrt water level
//    		if (TypeSurvey == "WLRS") {hGeoref = hGeoref + height_Ell_WL;}
//
//    		// distance water surface seafloor
//    		if (TypeSurvey == "InstantDepth"){hGeoref = rn3 + draft;}
//    	}
//
//    	// Transform to degres: We add HeightWL to h
//    	latGeoref = latGeoref*180/PI;
//    	lonGeoref = lonGeoref*180/PI;
//    	
//    };

}