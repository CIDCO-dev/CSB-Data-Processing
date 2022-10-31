package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.sql.Timestamp;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import ca.cidco.csb.surveydata.Position;
import ca.cidco.csb.surveyplatform.hydroblock.Hydroblock20;

public class Hydroblock20Test {
	Hydroblock20 hydro = new Hydroblock20();

	String dataPathValid = "data/hydroblockReadDataTest/completeData";
	
	String dataPathNoSonarFile = "data/hydroblockReadDataTest/noSonar/";
	String dataPathEmptySonarFile = "data/hydroblockReadDataTest/emptySonarFile/";
	String dataPathNoUbxFile = "data/hydroblockReadDataTest/noUbx/";
	String dataPathEmptyImuFile = "data/hydroblockReadDataTest/emptyImuFile/";
	String dataPathNoImuFile = "data/hydroblockReadDataTest/noImu/";
	String dataEmptyDirectory = "data/hydroblockReadDataTest/emptyDirectory/";

	@Test
	public void ReadValidTest() throws Exception {
		
		// assert attitudes, positions and depths clears 
		assertTrue(hydro.getAttitudes().size() ==0);
		assertTrue(hydro.getPositions().size()==0);
		assertTrue(hydro.getDepths().size()==0);
		assertFalse(hydro.getGnss().isErsValid());
		assertFalse(hydro.getGnss().isWlrsValid());
		
		hydro.read(dataPathValid);
		
		// assert attitudes, positions and depths not empty 
		assertTrue(hydro.getAttitudes().size() >0);
		assertTrue(hydro.getPositions().size()>0);
		assertTrue(hydro.getDepths().size()>0);
		// must be valid for ERS // WLRS
		assertTrue(hydro.getGnss().isErsValid());
		assertTrue(hydro.getGnss().isWlrsValid());
	}
	
	@Test (expected = Exception.class)
	public void ReadEmptyDirectoryPathTest() throws Exception {
		hydro.read(dataEmptyDirectory);
	}

	@Test (expected = Exception.class)
	public void ReadInvalidPathTest() throws Exception {
		hydro.read("data/hydroblockReadDataTest/notExistingFiles/");
	}
	
	@Test (expected = Exception.class)
	public void ReadPathWithoutSonarFileTest() throws Exception {
		hydro.read(dataPathNoSonarFile);
	}
	
	@Test (expected = Exception.class)
	public void ReadPathEmptySonarFileTest() throws Exception {
		hydro.read(dataPathEmptySonarFile);
	}
	
	@Test (expected = Exception.class)
	public void ReadPathWithoutImuFileTest() throws Exception {
		hydro.read(dataPathNoImuFile);
	}
	
	@Test (expected = Exception.class)
	public void ReadPathEmptyImuFileTest() throws Exception {
		hydro.read(dataPathEmptyImuFile);
	}
	@Test (expected = Exception.class)
	public void ReadPathWithoutUbxFileTest() throws Exception {
		hydro.read(dataPathNoUbxFile);
	}
	
	@Test
	public void setPositionsTest() throws Exception {
		
		ArrayList<Position> testPositions= new ArrayList<Position>();

		//Create valid positions 
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
		String dateTime= "2022-10-10 20:44:28.0";
		java.util.Date parsedDate = dateFormat.parse(dateTime);
		Timestamp timestamp = new java.sql.Timestamp(parsedDate.getTime());
		Position position = new Position(timestamp,50.1919, -66.40107, -0.0965,0.0347,0.0227 ,0.0546,12,1.8);
		
	    // adding 10 position to testPositions
	    for (int i =0; i<10; i++) {
	    	testPositions.add(position);
	    }
	    // set positions with the new Array (10x same position)
	    hydro.setPositions(testPositions);
	    
	    assertEquals(10, hydro.getPositions().size());
	}
}
