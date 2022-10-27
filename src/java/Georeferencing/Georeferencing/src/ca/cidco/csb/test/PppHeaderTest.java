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
}
