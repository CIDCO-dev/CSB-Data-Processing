package ca.cidco.csb;

import static org.junit.Assert.assertTrue;

import ca.cidco.csb.georeference.ErsGeoreferencing;
import ca.cidco.csb.georeference.Georeference;
import ca.cidco.csb.ppp.NrcanPPP;
import ca.cidco.csb.ppp.PppFile;
import ca.cidco.csb.surveyplatform.hydroblock.Hydroblock20;
import ca.cidco.csb.utilities.Conversion;

public class Main {

	public static void main(String[] args) {
		//TODO: Testing CLI 
		
    	// ubx test if no cli args

		String test9ubx = "/home/dominic/Bureau/georef/2022.10.11_224413.ubx"; // Valid 	 POS		Bella
		String test9imu = "/home/dominic/Bureau/georef/2022.10.11_223416_imu.txt"; 
		String test9sonar = "/home/dominic/Bureau/georef/2022.10.11_223416_sonar.txt"; 
		String test9 = "/home/dominic/Bureau/georef/"; 
		String test1 = "/home/dominic/Bureau/georef/test/"; 
		String test2 = "/home/dominic/Bureau/georef/test2/"; 
		String test3 = "/home/dominic/Bureau/georef/test3/"; 
		String ubx194410 = "/home/dominic/Bureau/ubx/2022.10.10_194410.ubx"; 
		
		
		//CLI args
/*		String gnssBinaryFile="";
		if (args.length > 0) 	
		    try {
		    	gnssBinaryFile = new java.io.File(args[0]).getAbsolutePath();
		    } catch (Exception e) {
		        System.err.println("Argument " + args[0] + " must be an Binary File.");
		        System.exit(1);
		    }
		}
		//If no valid args, use test File 
		else {
			gnssBinaryFile = test8;
			System.err.println("No arg in CLI, processing this test file :"+gnssBinaryFile);
		}
*/		
		// test9 is dataPath with imu sonar and ubx files
		try {
			NrcanPPP nrcan = new NrcanPPP(ubx194410);
			
			System.out.println(nrcan.getUbxFilePath());
			System.out.println(nrcan.getFileName());
			System.out.println(nrcan.getNameNoExt());
			System.out.println(nrcan.getUbxFileDirectory());
			System.out.println(nrcan.getWorkingDirectoryName());
			System.out.println(nrcan.getDirectoryRinexName());
			System.out.println(nrcan.getPppDirectoryName());

			
			
//			PppFile ppp= nrcan.fetchPPP("dominic.gonthier@cidco.ca");
//			System.err.println(ppp.getPositions().size());
			
			
//			System.out.println(Conversion.convertDMStoDecimalDegree(342.12, 48.234 , 56.4567));
//			Hydroblock20 hydro = new Hydroblock20();
//			hydro.read(test9);
			
						
//			ErsGeoreferencing georef = new ErsGeoreferencing();
//			System.out.println(georef.getClass());
//			georef.process(hydro.getPositions(), hydro.getAttitudes(), hydro.getDepths());
//			System.err.println(georef.getBathyPoints().size());

			
		}
		catch(Exception e) {
			System.err.println("Error while georeferencing: " + e.getMessage() );
		}
			

/*
		Georeferencing geo =new Georeferencing();
		geo.dcm(1.054, 4.25, 1.2458);
		
//		public void LatLonH_2_ECEF(double lat, double lon, double ellipsoidal_height, double half_ellipsoidal_axe, double first_eccentricity)
		geo.LatLonH_2_ECEF(46.86194, -4.470, 48.8, 6378137, 0.081819190842622);
*/		
		
		

	}
}