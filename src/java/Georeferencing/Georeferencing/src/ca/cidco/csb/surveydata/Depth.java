package ca.cidco.csb.surveydata;

import java.sql.Timestamp;

public class Depth{
	
	private Timestamp timestamp;
	
	private Double depth; // in meters
	
	public Depth(Timestamp timestamp_, Double depth_) {
		timestamp = timestamp_;
		depth = depth_;
		
	}

	public Timestamp getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(Timestamp timestamp) {
		this.timestamp = timestamp;
	}

	public Double getDepth() {
		return depth;
	}

	public void setDepth(Double depth) {
		this.depth = depth;
	}
	
    // Overriding toString() method of String class
    @Override
    public String toString() {
        return "timestamp : "+ timestamp+" |  depth : "+depth+"\n";
    }
}
