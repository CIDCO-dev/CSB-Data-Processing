package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import org.junit.Test;

import ca.cidco.csb.ppp.PppHeader;

public class PppHeaderTest {
	
	private String detectHeader(String posFile) throws Exception {
		
		File pppFile = new File(posFile);
		FileReader fileReaderData = new FileReader(pppFile);
		BufferedReader bufferedReader = new BufferedReader(fileReaderData);
		String row;
		String[] split_row;			
			
		while ((row = bufferedReader.readLine()) !=null )  {
			split_row= row.split("[\\s]{1,}");
			if(split_row[0].equalsIgnoreCase("DIR")){
				break;
			}
		}
		PppHeader header = new PppHeader(row); 
		return header.getDetectedHeader();
	}
	
	String PPP_HEADER_1 = "DIR FRAME        STN         DOY YEAR-MM-DD HR:MN:SS.SSS NSV GDOP    SDC    SDP       DLAT(m)       DLON(m)       DHGT(m)         CLK(ns)   TZD(m)  SLAT(m)  SLON(m)  SHGT(m) SCLK(ns)  STZD(m) LAT(d) LAT(m)    LAT(s) LON(d) LON(m)    LON(s)   HGT(m) CGVD28_HTv2.0_Height NORTHING(m)  EASTING(m) ZONE SCALE_FACTOR HEMI   AM COMBINED_SCALE_FACTOR ";
	String PPP_HEADER_2 = "DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m)          CLK(ns)  TZD(m) SDLAT(95%) SDLON(95%) SDHGT(95%) SDCLK(95%) SDTZD(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m)";
	String PPP_HEADER_3 = "DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m) SDLAT(95%) SDLON(95%) SDHGT(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m) SIGLAT_TOT(95%) SIGLON_TOT(95%) SIGHGT_TOT(95%)";
	String PPP_HEADER_4 = "DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m)          CLK(ns)  TZD(m) SDLAT(95%) SDLON(95%) SDHGT(95%) SDCLK(95%) SDTZD(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m) SIGLAT_TOT(95%) SIGLON_TOT(95%) SIGHGT_TOT(95%)";
	String PPP_HEADER_5 =	"DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m) SDLAT(95%) SDLON(95%) SDHGT(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD2013(m)";
  	
	
	PppHeader headerNoArg = new PppHeader();
	PppHeader headerTest = new PppHeader("DIR FRAME  STN   DAYofYEAR YEAR-MM-DD HR:MN:SS.SS NSV GDOP RMSC(m) RMSP(m)       DLAT(m)       DLON(m)       DHGT(m)          CLK(ns)  TZD(m) SDLAT(95%) SDLON(95%) SDHGT(95%) SDCLK(95%) SDTZD(95%) LATDD LATMN    LATSS LONDD LONMN    LONSS     HGT(m) UTMZONE    UTM_EASTING   UTM_NORTHING UTM_SCLPNT UTM_SCLCBN MTMZONE    MTM_EASTING   MTM_NORTHING MTM_SCLPNT MTM_SCLCBN H:CGVD28(m) SIGLAT_TOT(95%) SIGLON_TOT(95%) SIGHGT_TOT(95%)"
);
	
	// files to test	                          		          	file header
	String file1 = "data/posHeader/file1.pos"; 						//3
	String file2 = "data/posHeader/file2.pos"; 						//5
	String file3 = "data/posHeader/file3.pos"; 						//3
	String file4 = "data/posHeader/file4.pos"; 						//2
	String TestPPP = "data/posHeader/TestPPP.pos";					//1
	String TestPPPFormat1 = "data/posHeader/TestPPPFormat1.pos";	//1
	String TestPPPFormat2 = "data/posHeader/TestPPPFormat2.pos";	//2
	String TestPPPFormat3 = "data/posHeader/TestPPPFormat3.pos";	//3

	@Test
	public void detectHeader1Test() throws Exception {
		
		assertTrue(detectHeader(TestPPPFormat1).equals("PPP_HEADER_1"));
		assertFalse(detectHeader(file2).equals("PPP_HEADER_1"));
		assertTrue(detectHeader(TestPPP).equals("PPP_HEADER_1"));
	}
	
	@Test
	public void detectHeader2Test() throws Exception {

		assertTrue(detectHeader(TestPPPFormat2).equals("PPP_HEADER_2"));
		assertFalse(detectHeader(file2).equals("PPP_HEADER_2"));
		assertTrue(detectHeader(file4).equals("PPP_HEADER_2"));
	}
	
	@Test
	public void detectHeader3Test() throws Exception {

		assertTrue(detectHeader(file1).equals("PPP_HEADER_3"));
		assertFalse(detectHeader(file2).equals("PPP_HEADER_3"));
		assertTrue(detectHeader(file3).equals("PPP_HEADER_3"));
	}
	
	@Test
	public void detectHeader4Test() throws Exception {

		assertFalse(detectHeader(file1).equals("PPP_HEADER_4"));
		assertFalse(detectHeader(file2).equals("PPP_HEADER_4"));
	}
	
	@Test
	public void detectHeader5Test() throws Exception {

		assertTrue(detectHeader(file2).equals("PPP_HEADER_5"));
		assertFalse(detectHeader(TestPPPFormat3).equals("PPP_HEADER_5"));
	}
	
	@Test
	public void toStringTest() {
		
		String headerString = headerTest.toString();
		assertTrue(headerString.contains("date"));
		assertTrue(headerString.contains("time"));
		assertTrue(headerString.contains("nsv"));
		assertTrue(headerString.contains("gdop"));
		assertTrue(headerString.contains("sdlat"));
		assertTrue(headerString.contains("sdlon"));
		assertTrue(headerString.contains("sdhgt"));
	}

	@Test
	public void getDateIndexTest() {
		assertEquals(4,headerTest.getDateIndex()); 
	}
	
	@Test
	public void getTimeIndexTest() {
		assertEquals(5,headerTest.getTimeIndex()); 
	}
	
	@Test
	public void getNsvIndexTest() {
		assertEquals(6,headerTest.getNsvIndex()); 
	}
	
	@Test
	public void getGdopIndexTest() {
		assertEquals(7,headerTest.getGdopIndex()); 
	}
	
	@Test
	public void getSdlatIndexTest() {
		assertEquals(15,headerTest.getSdlatIndex()); 
	}
	
	@Test
	public void getSdlonIndexTest() {
		assertEquals(16,headerTest.getSdlonIndex()); 
	}
	
	@Test
	public void getSdhgtIndexTest() {
		assertEquals(17,headerTest.getSdhgtIndex()); 
	}
	
	@Test
	public void getLatDdIndexTest() {
		assertEquals(20,headerTest.getLatDdIndex()); 
	}
	
	@Test
	public void getLatMnIndexTest() {
		assertEquals(21,headerTest.getLatMnIndex());
	}
	
	@Test
	public void getLatSsIndexTest() {
		assertEquals(22,headerTest.getLatSsIndex());
	}
	
	@Test
	public void getLonDdIndexTest() {
		assertEquals(23,headerTest.getLonDdIndex());
	}
	
	@Test
	public void getLonMnIndexTest() {
		assertEquals(24,headerTest.getLonMnIndex());
	}
	
	@Test
	public void getLonSsIndexTest() {
		assertEquals(25,headerTest.getLonSsIndex());
	}
	
	@Test
	public void getHgtIndexTest() {
		assertEquals(26,headerTest.getHgtIndex());
	}
	
	@Test
	public void getDetectedHeaderTest() {
		assertTrue(headerTest.getDetectedHeader()=="PPP_HEADER_4");
	}
	
	@Test
	public void getPPP_HEADER_1Test() {
		assertTrue(headerNoArg.getPPP_HEADER_1()==PPP_HEADER_1);
		assertTrue(headerNoArg.getPPP_HEADER_2()==PPP_HEADER_2);
		assertTrue(headerNoArg.getPPP_HEADER_3()==PPP_HEADER_3);
		assertTrue(headerNoArg.getPPP_HEADER_4()==PPP_HEADER_4);
		assertTrue(headerNoArg.getPPP_HEADER_5()==PPP_HEADER_5);
	}	
}
