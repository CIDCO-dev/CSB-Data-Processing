package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.sql.Timestamp;

import org.junit.Test;

import ca.cidco.csb.surveydata.Attitude;
import ca.cidco.csb.surveydata.Depth;

public class AttitudeTest {

	Timestamp timestamp= 	new Timestamp(1527636114); 
	Attitude attitude = new Attitude(timestamp, 133.0 , 18.8, -46.0 );
	

	@Test
	public void testGetTimestamp() {
		assertEquals(1527636114, attitude.getTimestamp().getTime());
	}

	@Test
	public void testSetTimestamp() {
		Timestamp t2 = new Timestamp(1527777777);
		attitude.setTimestamp(t2);
		assertEquals(1527777777, attitude.getTimestamp().getTime());	
	}

	@Test
	public void testGetHeading() {
		assertTrue(133.0 == attitude.getHeading());
	}

	@Test
	public void testSetHeading() {
		attitude.setHeading(126.42);
		assertTrue(126.42 == attitude.getHeading());		}

	@Test
	public void testGetPitch() {
		assertTrue(18.8 == attitude.getPitch());
	}

	@Test
	public void testSetPitch() {
		attitude.setPitch(21.42);
		assertTrue(21.42 == attitude.getPitch());	
	}

	@Test
	public void testGetRoll() {
		assertTrue(-46.0 == attitude.getRoll());
	}

	@Test
	public void testSetRoll() {
		attitude.setRoll(-42.42);
		assertTrue(-42.42 == attitude.getRoll());	
	}

	@Test
	public void testToString() {
		String attitudeString = attitude.toString();
		assertTrue(attitudeString.contains(attitude.getHeading().toString()));
		assertTrue(attitudeString.contains(attitude.getPitch().toString()));
		assertTrue(attitudeString.contains(attitude.getRoll().toString()));
		assertTrue(attitudeString.contains(attitude.getTimestamp().toString()));
	}
}
