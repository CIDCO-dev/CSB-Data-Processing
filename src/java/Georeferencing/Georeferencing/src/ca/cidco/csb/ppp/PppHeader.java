package ca.cidco.csb.ppp;

import java.io.BufferedReader;
import java.io.FileReader;
import java.math.BigDecimal;
import java.sql.Timestamp;
import java.util.Date;

public class PppHeader {

	private String detectedHeader = "";
	private int dateIndex = 0;
	private int timeIndex = 0;
	private int nsvIndex = 0;
	private int gdopIndex = 0;
	private int sdlatIndex = 0;
	private int sdlonIndex = 0;
	private int sdhgtIndex = 0;
	private int latDdIndex = 0;  //  degres  
	private int latMnIndex = 0;  //  minutes 
	private int latSsIndex = 0;  //  secondes
	private int lonDdIndex = 0;  //  degres  
	private int lonMnIndex = 0;  //  minutes 
	private int lonSsIndex = 0;  //  secondes
	private int hgtIndex = 0;  // meters

	public static String PPP_HEADER_1 = "DIR FRAME        STN         DOY YEAR-MM-DD HR:MN:SS.SSS NSV GDOP    SDC    SDP       DLAT(m)       DLON(m)       DHGT(m)         CLK(ns)   TZD(m)  SLAT(m)  SLON(m)  SHGT(m) SCLK(ns)  STZD(m) LAT(d) LAT(m)    LAT(s) LON(d) LON(m)    LON(s)   HGT(m) CGVD28_HTv2.0_Height NORTHING(m)  EASTING(m) ZONE SCALE_FACTOR HEMI   AM COMBINED_SCALE_FACTOR ";
	public static String PPP_HEADER_2 = "DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m)          CLK(ns)  TZD(m) SDLAT(95%) SDLON(95%) SDHGT(95%) SDCLK(95%) SDTZD(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m)";
	public static String PPP_HEADER_3 = "DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m) SDLAT(95%) SDLON(95%) SDHGT(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m) SIGLAT_TOT(95%) SIGLON_TOT(95%) SIGHGT_TOT(95%)";
	public static String PPP_HEADER_4 = "DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m)          CLK(ns)  TZD(m) SDLAT(95%) SDLON(95%) SDHGT(95%) SDCLK(95%) SDTZD(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m) SIGLAT_TOT(95%) SIGLON_TOT(95%) SIGHGT_TOT(95%)";
	public static String PPP_HEADER_5 =	"DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m) SDLAT(95%) SDLON(95%) SDHGT(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD2013(m)";
  
	public PppHeader() {
		// Auto-generated constructor to initialize

	}
	// Match the header and set the index
	public PppHeader(String row) {
//		System.out.println("row          :" + row);

		if (PPP_HEADER_1.contains(row)) {
			dateIndex = 4; timeIndex = 5;	nsvIndex = 6; gdopIndex = 7; sdlatIndex = 15; sdlonIndex = 16; sdhgtIndex = 17;
			latDdIndex=20; latMnIndex=21; latSsIndex=22; lonDdIndex=23; lonMnIndex=24; lonSsIndex=25; hgtIndex=26;
			detectedHeader = "PPP_HEADER_1";

		} else if (PPP_HEADER_2.contains(row)) {
			dateIndex = 4; timeIndex = 5; nsvIndex = 6; gdopIndex = 7; sdlatIndex = 15; sdlonIndex = 16; sdhgtIndex = 17;
			latDdIndex=20; latMnIndex=21; latSsIndex=22; lonDdIndex=23; lonMnIndex=24; lonSsIndex=25; hgtIndex=26;
			detectedHeader = "PPP_HEADER_2";

		} else if (PPP_HEADER_3.contains(row)) {
			dateIndex = 4; timeIndex = 5; nsvIndex = 6; gdopIndex = 7; sdlatIndex = 13; sdlonIndex = 14; sdhgtIndex = 15;
			latDdIndex=16; latMnIndex=17; latSsIndex=18; lonDdIndex=19; lonMnIndex=20; lonSsIndex=21; hgtIndex=22;
			detectedHeader = "PPP_HEADER_3";

		} else if (PPP_HEADER_4.contains(row)) {
			dateIndex = 4; timeIndex = 5; nsvIndex = 6; gdopIndex = 7; sdlatIndex = 15; sdlonIndex = 16; sdhgtIndex = 17;
			latDdIndex=20; latMnIndex=21; latSsIndex=22; lonDdIndex=23; lonMnIndex=24; lonSsIndex=25; hgtIndex=26;
			detectedHeader = "PPP_HEADER_4";
			
		} else if (PPP_HEADER_5.contains(row)) {
			dateIndex = 4; timeIndex = 5; nsvIndex = 6; gdopIndex = 7; sdlatIndex = 13; sdlonIndex = 14; sdhgtIndex = 15;
			latDdIndex=16; latMnIndex=17; latSsIndex=18; lonDdIndex=19; lonMnIndex=20; lonSsIndex=21; hgtIndex=22;
			detectedHeader = "PPP_HEADER_5";

		} else {
			System.out.println("unknow header");
		}
	}


	@Override
	public String toString() {
		String output = "header_index: \n";
		output += "date :" + dateIndex + " | ";
		output += "time :" + timeIndex + " | ";
		output += "nsv : " + nsvIndex + " | ";
		output += "gdop :" + gdopIndex + " | ";
		output += "sdlat :" + sdlatIndex + " | ";
		output += "sdlon :" + sdlonIndex + " | ";
		output += "sdhgt :" + sdhgtIndex + " | ";

		return output;
	}
	public int getDateIndex() {
		return dateIndex;
	}
	public int getTimeIndex() {
		return timeIndex;
	}
	public int getNsvIndex() {
		return nsvIndex;
	}
	public int getGdopIndex() {
		return gdopIndex;
	}
	public int getSdlatIndex() {
		return sdlatIndex;
	}
	public int getSdlonIndex() {
		return sdlonIndex;
	}
	public int getSdhgtIndex() {
		return sdhgtIndex;
	}
	public int getLatDdIndex() {
		return latDdIndex;
	}
	public int getLatMnIndex() {
		return latMnIndex;
	}
	public int getLatSsIndex() {
		return latSsIndex;
	}
	public int getLonDdIndex() {
		return lonDdIndex;
	}
	public int getLonMnIndex() {
		return lonMnIndex;
	}
	public int getLonSsIndex() {
		return lonSsIndex;
	}
	public int getHgtIndex() {
		return hgtIndex;
	}
	public String getDetectedHeader() {
		return detectedHeader;
	}
	public static String getPPP_HEADER_1() {
		return PPP_HEADER_1;
	}
	public static String getPPP_HEADER_2() {
		return PPP_HEADER_2;
	}
	public static String getPPP_HEADER_3() {
		return PPP_HEADER_3;
	}
	public static String getPPP_HEADER_4() {
		return PPP_HEADER_4;
	}
	public static String getPPP_HEADER_5() {
		return PPP_HEADER_5;
	}

}
