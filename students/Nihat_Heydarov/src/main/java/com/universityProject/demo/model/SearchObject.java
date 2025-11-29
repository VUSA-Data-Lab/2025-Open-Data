package com.universityProject.demo.model;

public class SearchObject{
	private String municipality;
	private String year;
	
	public SearchObject() {
		
	}
	public SearchObject(String municipality, String year) {
		this.municipality=municipality;
		this.year =year;
	}
	public String getMunicipality() {
		return municipality;
	}
	public void setMunicipality(String municipality) {
		this.municipality=municipality;
	}
	public String getYear() {
		return year;
	}
	public void setYear(String year) {
		this.year=year;
	}
}