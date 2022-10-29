package ca.cidco.csb.georeference;

import java.sql.Timestamp;

public class BathymetryPoint {
	
	private Timestamp timestamp;
	private Double longitude;
	private Double latitude;
	private Double ellipsoidalHeight;
	private Double sdLongitude;
	private Double sdLatitude;
	private Double sdEllipsoidalHeight;
	
	public BathymetryPoint(Timestamp timestamp,	 Double longitude, Double latitude, Double ellipsoidalHeight, Double sdLongitude, Double sdLatitude, Double sdEllipsoidalHeight) {
		this.timestamp= timestamp;
		this.longitude= longitude;
		this.latitude= latitude;
		this.ellipsoidalHeight= ellipsoidalHeight;
		this.sdLongitude= sdLongitude;
		this.sdLatitude= sdLatitude;
		this.sdEllipsoidalHeight= sdEllipsoidalHeight;
	}

	
	public Timestamp getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(Timestamp timestamp) {
		this.timestamp = timestamp;
	}

	public Double getSdLongitude() {
		return sdLongitude;
	}

	public void setSdLongitude(Double sdLongitude) {
		this.sdLongitude = sdLongitude;
	}

	public Double getSdLatitude() {
		return sdLatitude;
	}

	public void setSdLatitude(Double sdLatitude) {
		this.sdLatitude = sdLatitude;
	}

	public Double getSdEllipsoidalHeight() {
		return sdEllipsoidalHeight;
	}

	public void setSdEllipsoidalHeight(Double sdEllipsoidalHeight) {
		this.sdEllipsoidalHeight = sdEllipsoidalHeight;
	}


	public Double getLongitude() {
		return longitude;
	}

	public void setLongitude(Double longitude) {
		this.longitude = longitude;
	}

	public Double getLatitude() {
		return latitude;
	}

	public void setLatitude(Double latitude) {
		this.latitude = latitude;
	}

	public Double getEllipsoidalHeight() {
		return ellipsoidalHeight;
	}

	public void setEllipsoidalHeight(Double ellipsoidalHeight) {
		this.ellipsoidalHeight = ellipsoidalHeight;
	}
	
    // Overriding toString() method of String class
    @Override
    public String toString() {
        return "Timestamp : "+ timestamp+" |  Longitude : "+longitude+" | Latitude : "+ latitude +" | height : "+ellipsoidalHeight +"   | SDLAT : "+sdLatitude+" | SDLON : "+sdLongitude+" | SDHGT : "+sdEllipsoidalHeight +"\n";
    }
}
