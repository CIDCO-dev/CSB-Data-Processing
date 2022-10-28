package ca.cidco.csb.test;

import static org.junit.Assert.*;

import java.math.BigDecimal;
import java.math.MathContext;

import org.junit.Test;

import ca.cidco.csb.utilities.BigDecimalFactory;

public class BigDecimalFactoryTest {
	
	BigDecimal compare = new BigDecimal(12.123454999999999870, new MathContext(20)); 
	
	
	@Test
	public void testCreateStringDecimal() {
		BigDecimal big= BigDecimalFactory.create("12.123454999999999870");
		assertTrue(big.getClass().getName().toString()== "java.math.BigDecimal");
		assertTrue(compare.equals(big));
	}
	
	@Test
	public void testCreateStringInteger() {
		BigDecimal big= BigDecimalFactory.create("12345499");
		assertTrue(big.getClass().getName().toString()== "java.math.BigDecimal");
	}

	@Test
	public void testCreateDouble() {
		BigDecimal big= BigDecimalFactory.create(12.1234);
		assertTrue(big.getClass().getName().toString()== "java.math.BigDecimal");
	}

	@Test
	public void testCreateLong() {
		BigDecimal big= BigDecimalFactory.create(42L);
		assertTrue(big.getClass().getName().toString()== "java.math.BigDecimal");
	}
}
