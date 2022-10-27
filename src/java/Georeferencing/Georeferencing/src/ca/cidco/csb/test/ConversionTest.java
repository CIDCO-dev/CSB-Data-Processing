package ca.cidco.csb.test;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import ca.cidco.csb.utilities.Conversion;
import junit.framework.AssertionFailedError;

public class ConversionTest {


	@Test
	public void testConvertDMStoDecimalDegree() throws Exception {
		double result =Conversion.convertDMStoDecimalDegree(32.4, 48.234 , 56.456);
		assertTrue((33.21958-0.00001)< result && result <33.21958+0.00001);
		// Same with negative degrees
		double result_neg =Conversion.convertDMStoDecimalDegree(-32.4, 48.234 , 56.456);
		assertTrue((-33.21958-0.00001)< result_neg && result_neg <-33.21958+0.00001);
			
		double result_1 =Conversion.convertDMStoDecimalDegree(12.456, 18.234 , 6.456);
		assertTrue((12.76169-0.00001)< result_1 && result_1 <12.76169+0.00001);
	}
	
	@Test
	public void testConvertDMStoDecimalDegree_DegreesOutOfBound() {
		try {
			Conversion.convertDMStoDecimalDegree(412.456, 28.234 , 6.456);
			fail( "Didn't detect out of Bound degrees ");
		}
		catch (Exception e){
//			this is good
		}
	}
	
	@Test
	public void testConvertDMStoDecimalDegree_MinutesOutOfBound() {
		try {
			Conversion.convertDMStoDecimalDegree(12.456, 68.234 , 6.456);
			fail( "Didn't detect out of Bound minutes" );
		}
		catch (Exception e) {
//			this is good
		}
	}
	
	@Test
	public void testConvertDMStoDecimalDegree_SecondesOutOfBound() {
		try {
			Conversion.convertDMStoDecimalDegree(12.456, 48.234 , 74.457);
			fail( "Didn't detect out of Bound secondes" );
		}
		catch (IllegalArgumentException e) {
//			this is good
		}
	}
	@Test
	public void testConvertDMStoDecimalDegree_NegativesSecondesValue() {
		try {
			Conversion.convertDMStoDecimalDegree(12.456, 8.234 , -12.457);
			fail( "Didn't detect negative secondes values" );
		}
		catch (IllegalArgumentException e) {
//			this is good
		}
	}
	
	@Test
	public void testConvertDMStoDecimalDegree_NegativesMinutesValue() {
		try {
			Conversion.convertDMStoDecimalDegree(12.456, -42.234 , 12.457);
			fail( "Didn't detect negative minutes values" );
		}
		catch (IllegalArgumentException e) {
//			this is good
		}
	}

}
