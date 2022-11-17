/*
 * Copyright 2017 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
 */

package ca.cidco.csb.utilities;


import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

/**
 *
 * @author jordan
 */

public class BigDecimalFactory {

    public static final MathContext mc = new MathContext(20);

    public static BigDecimal create(String s) {
        String[] splitOnDecimalPoint = s.split("\\.");
        if (splitOnDecimalPoint.length == 2) {
            return new BigDecimal(s, mc).setScale(splitOnDecimalPoint[1].length(), RoundingMode.HALF_UP);
        } else {
            return new BigDecimal(s, mc).setScale(0, RoundingMode.HALF_UP);
        }
    }

    public static BigDecimal create(Double b) {
        return new BigDecimal(b, mc).setScale(20, RoundingMode.HALF_UP);
    }

    public static BigDecimal create(Long l) {
        return new BigDecimal(l, mc).setScale(20, RoundingMode.HALF_UP);
    }
}


