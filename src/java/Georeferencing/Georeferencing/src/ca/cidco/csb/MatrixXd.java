package ca.cidco.csb;

import java.util.Scanner;

public class MatrixXd {
	double[][] a = new double[3][3];
	
	
	MatrixXd() {
		
	}
	
	public void initializeMatrixXd(double cR, double sR, double cP, double sP, double cY, double sY) {
		a[0][0]=(cY*cP);
		a[0][1]=(cY*sP*sR-cR*sY);
		a[0][2]=(cY*cR*sP+sR*sY);
		a[1][0]=(cP*sY);
		a[1][1]=(cY*cR+sP*sR*sY);
		a[1][2]=(sY*cR*sP-cY*sR);
		a[2][0]=(-sP);
		a[2][1]=(cP*sR);
		a[2][2]=(cR*cP);
		
		printMatrix(this);
	}
	

	
	
	public void printMatrix(MatrixXd m) {
		System.out.println("Matrix initialized: \n");
		for( int i = 0; i<3; i++) {
			for( int j = 0; j<3; j++) {
				System.out.print( a[i][j]+"	");
			}
			System.out.println("	");
		}
		System.out.println("	");
	}
	
	
}