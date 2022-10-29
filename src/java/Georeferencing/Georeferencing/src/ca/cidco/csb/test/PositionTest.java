package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.sql.Timestamp;

import org.junit.Test;

import ca.cidco.csb.surveydata.Attitude;
import ca.cidco.csb.surveydata.Position;

public class PositionTest {

	Timestamp timestamp= 	new Timestamp(1527636114); 
//	Pos1(timestamp, long_D, long_MN, long_SS, lat_D, lat_MN, lat_SS, height, sdLong, sdLat, sdHeight,  nsv,  gdop_)
	Position positionDMS = new Position(timestamp, -68.0 , 31.0, 58.24653, 48.0 , 26.0, 55.83051, -38.2119,  3.2922 , 2.8830, 7.3211, 8L, 3.6);
//	Pos2(timestamp, Lat, Long, Height, sdLat, sdLong, sdHeight, nsv, gdop) {
	Position positionDD = new Position(timestamp, 48.44884, -68.53285, -38.2119, 2.8830, 3.2922 , 7.3211, 8L, 3.6);
	

	@Test
	public void testGetLongitude() {
		assertTrue(positionDD.getLongitude()==-68.53285);
		assertTrue(positionDMS.getLongitude()<-68.53285+00001 && positionDMS.getLongitude()>-68.53285-00001 );
	}

	@Test
	public void testSetLongitude() {
		positionDMS.setLongitude(42.7777);
		assertTrue(42.7777== positionDMS.getLongitude());
		positionDD.setLongitude(42.7777);
		assertTrue(42.7777== positionDD.getLongitude());
	}

	@Test
	public void testGetLatitude() {
		assertTrue(positionDD.getLatitude()==48.44884);
		assertTrue(positionDMS.getLatitude()<48.44884+00001 && positionDMS.getLatitude()>48.44884-00001 );
	}

	@Test
	public void testSetLatitude() {
		positionDMS.setLatitude(42.7777);
		assertTrue(42.7777== positionDMS.getLatitude());
		positionDD.setLatitude(42.7777);
		assertTrue(42.7777== positionDD.getLatitude());	
	}

	@Test
	public void testGetTimestamp() {
		assertTrue(positionDD.getTimestamp().getTime()== 1527636114);
		assertTrue(positionDMS.getTimestamp().getTime()== 1527636114);	
	}

	@Test
	public void testSetTimestamp() {
		Timestamp testTime = new Timestamp(1234567890);
		positionDMS.setTimestamp(testTime);
		assertTrue(1234567890== positionDMS.getTimestamp().getTime());
		positionDD.setTimestamp(testTime);
		assertTrue(1234567890== positionDD.getTimestamp().getTime());	
	}

	@Test
	public void testGetHeight() {
		assertTrue(positionDD.getHeight()==-38.2119);
		assertTrue(positionDMS.getHeight()==-38.2119);
	}

	@Test
	public void testSetHeight() {
		positionDMS.setHeight(42.7777);
		assertTrue(42.7777== positionDMS.getHeight());
		positionDD.setHeight(42.7777);
		assertTrue(42.7777== positionDD.getHeight());	

	}

	@Test
	public void testGetSdLongitude() {
		assertTrue(positionDD.getSdLongitude()==3.2922);
		assertTrue(positionDMS.getSdLongitude()==3.2922);
	}

	@Test
	public void testSetSdLongitude() {
		positionDMS.setSdLongitude(2.7777);
		assertTrue(2.7777== positionDMS.getSdLongitude());
		positionDD.setSdLongitude(2.7777);
		assertTrue(2.7777== positionDD.getSdLongitude());	
	}

	@Test
	public void testGetSdLatitude() {
		assertTrue(positionDD.getSdLatitude()== 2.8830);
		assertTrue(positionDMS.getSdLatitude()== 2.8830);
	}

	@Test
	public void testSetSdLatitude() {
		positionDMS.setSdLatitude(4.2);
		assertTrue(4.2== positionDMS.getSdLatitude());
		positionDD.setSdLatitude(4.2);
		assertTrue(4.2== positionDD.getSdLatitude());			
	}

	@Test
	public void testGetSdHeight() {
		assertTrue(positionDD.getSdHeight()== 7.3211);
		assertTrue(positionDMS.getSdHeight()== 7.3211);
	}

	@Test
	public void testSetSdHeight() {
		positionDMS.setSdHeight(0.7777);
		assertTrue(0.7777== positionDMS.getSdHeight());
		positionDD.setSdHeight(0.7777);
		assertTrue(0.7777== positionDD.getSdHeight());	
	}

	@Test
	public void testGetNumberOfSatellites() {
		assertTrue(positionDD.getNumberOfSatellites()== 8);
		assertTrue(positionDMS.getNumberOfSatellites()== 8);
	}

	@Test
	public void testSetNumberOfSatellites() {
		positionDMS.setNumberOfSatellites(91L);
		assertTrue(91== positionDMS.getNumberOfSatellites());
		positionDD.setNumberOfSatellites(94L);
		assertTrue(94== positionDD.getNumberOfSatellites());
	}

	@Test
	public void testGetGdop() {
		assertTrue(positionDD.getGdop()== 3.6);
		assertTrue(positionDMS.getGdop()== 3.6);
	}

	@Test
	public void testSetGdop() {
		positionDMS.setGdop(0.42);
		assertTrue(0.42== positionDMS.getGdop());
		positionDD.setGdop(4.2);
		assertTrue(4.2== positionDD.getGdop());
	}

	@Test
	public void testToString() {
		String posDMS = positionDMS.toString();
		String posDD = positionDD.toString();
		assertTrue(posDMS.contains(positionDMS.getLatitude().toString()));
		assertTrue(posDMS.contains(positionDMS.getLongitude().toString()));
		assertTrue(posDMS.contains(positionDMS.getHeight().toString()));
		assertTrue(posDMS.contains(positionDMS.getNumberOfSatellites().toString()));
		assertTrue(posDMS.contains(positionDMS.getTimestamp().toString()));
		
		assertTrue(posDD.contains(positionDD.getLatitude().toString()));
		assertTrue(posDD.contains(positionDD.getLongitude().toString()));
		assertTrue(posDD.contains(positionDD.getHeight().toString()));
		assertTrue(posDD.contains(positionDD.getNumberOfSatellites().toString()));
		assertTrue(posDD.contains(positionDD.getTimestamp().toString()));
	}
}
