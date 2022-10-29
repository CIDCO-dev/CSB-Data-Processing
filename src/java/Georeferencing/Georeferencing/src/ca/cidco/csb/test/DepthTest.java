package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.sql.Timestamp;

import org.junit.Test;

import ca.cidco.csb.surveydata.Depth;

public class DepthTest {
	Timestamp timestamp= 	new Timestamp(1527636114); 
	Depth depth = new Depth(timestamp, 3.24);

	@Test
	public void testGetTimestamp() {
		assertEquals(1527636114, depth.getTimestamp().getTime());
	}

	@Test
	public void testSetTimestamp() {
		Timestamp t2 = new Timestamp(1527777777);
		depth.setTimestamp(t2);
		assertEquals(1527777777, depth.getTimestamp().getTime());
	}

	@Test
	public void testGetDepth() {
		assertTrue(3.24 == depth.getDepth());	
	}

	@Test
	public void testSetDepth() {
		depth.setDepth(42.42);
		assertTrue(42.42 == depth.getDepth());	
	}

	@Test
	public void testToString() {
		String depthString = depth.toString();
		assertTrue(depthString.contains("3.24"));
		assertTrue(depthString.contains(timestamp.toString()));
	}
}
