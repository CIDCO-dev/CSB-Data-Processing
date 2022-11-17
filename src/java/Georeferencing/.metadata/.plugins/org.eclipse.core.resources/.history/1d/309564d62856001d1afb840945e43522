package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.sql.Timestamp;
import java.text.ParseException;
import java.text.SimpleDateFormat;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import ca.cidco.csb.GnssQualifier;
import ca.cidco.csb.ppp.PppFile;
import ca.cidco.csb.surveydata.Position;

public class GnssQualifierTest {
	
	private Position buildValid() throws Exception {
		//Create timestamp to make positions 
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
		String dateTime= "2022-10-10 20:44:28.0";
		java.util.Date parsedDate = dateFormat.parse(dateTime);
		Timestamp timestamp = new java.sql.Timestamp(parsedDate.getTime());
		
		return new Position(timestamp,50.1919, -66.40107, -0.0965,0.0347,0.0227 ,0.0546,12,1.8);
	}
	

	@Test
	public void testValid() throws Exception {
		PppFile ppp = new PppFile();
		Position position = buildValid();
		ppp.getPositions().add(position);
		GnssQualifier gnss = new GnssQualifier();
		gnss.validate(ppp);
		
		assertTrue(gnss.isErsValid());
		assertTrue(gnss.isWlrsValid());
	}
	
	@Test
	public void testInvalidLatitude() throws Exception{
		PppFile ppp = new PppFile();
		Position position = buildValid();
		position.setSdLatitude(42.0254);
		ppp.getPositions().add(position);
		GnssQualifier gnss = new GnssQualifier();
		gnss.validate(ppp);
		
		assertFalse(gnss.isErsValid());
		assertFalse(gnss.isWlrsValid());
	}
	
	@Test
	public void testInvalidLongitude() throws Exception {
		PppFile ppp = new PppFile();
		Position position = buildValid();
		position.setSdLongitude(42.0254);
		ppp.getPositions().add(position);
		GnssQualifier gnss = new GnssQualifier();
		gnss.validate(ppp);
		
		assertFalse(gnss.isErsValid());
		assertFalse(gnss.isWlrsValid());	
	}
	
	@Test
	public void testInvalidHeight() throws Exception {
		PppFile ppp = new PppFile();
		Position position = buildValid();
		position.setSdHeight(42.0254);
		ppp.getPositions().add(position);
		GnssQualifier gnss = new GnssQualifier();
		gnss.validate(ppp);
		
		assertFalse(gnss.isErsValid());
		assertTrue(gnss.isWlrsValid());	
	}
	
	@Test
	public void testInvalidGdop() throws Exception {
		PppFile ppp = new PppFile();
		Position position = buildValid();
		position.setGdop(42.0254);
		ppp.getPositions().add(position);
		GnssQualifier gnss = new GnssQualifier();
		gnss.validate(ppp);
		
		assertFalse(gnss.isErsValid());
		assertFalse(gnss.isWlrsValid());	
	}
	
	@Test
	public void testInvalidNsv() throws Exception {
		PppFile ppp = new PppFile();
		Position position = buildValid();
		position.setNumberOfSatellites(2L);
		ppp.getPositions().add(position);
		GnssQualifier gnss = new GnssQualifier();
		gnss.validate(ppp);
		
		assertFalse(gnss.isErsValid());
		assertFalse(gnss.isWlrsValid());	
	}
	
	
}

