package com.universityProject.demo.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class TrafficVehicles{
	@JsonProperty("tpId")
	private int vehicleId;
	@JsonProperty("regValstybe")
	private String registrationCountry;
	@JsonProperty("kategorija")
	private String category;
	@JsonProperty("klase")
	private String classV;
	@JsonProperty("marke")
	private String make;
	@JsonProperty("modelis")
	private String model;
	@JsonProperty("pagaminimoMetai")
	private int manufactureYear;
	@JsonProperty("pasisalino")
	private String fledScene;
	@JsonProperty("ypatumai")
	private String features;
	@JsonProperty("apgadinimai")
	private String damages;
	@JsonProperty("apgadinimaiKita")
	private String otherDamages;
	@JsonProperty("apdraustasCivilines")
	private int insuredThirdParty;
	@JsonProperty("apdraustasKasko")
	private int insuredComprehensive;
	@JsonProperty("fizinis")
	private String physical;
	@JsonProperty("dalyvautiVTUzdrausta")
	private String participationProhibited;
	@JsonProperty("nuliamiantysGedimai")
	private String[] criticalDefects;
	@JsonProperty("pirminiaiSmugiai")
	private String[] initialImpacts;
	
	public TrafficVehicles() {
		
	}
	
	public TrafficVehicles(int vehicleId, String registrationCountry, String category, String classV, String make,
			String model, int manufactureYear, String fledScene, String features, String damages, String otherDamages,
			int insuredThirdParty, int insuredComprehensive, String physical, String participationProhibited,
			String[] criticalDefects, String[] initialImpacts) {
		
		this.vehicleId = vehicleId;
		this.registrationCountry = registrationCountry;
		this.category = category;
		this.classV = classV;
		this.make = make;
		this.model = model;
		this.manufactureYear = manufactureYear;
		this.fledScene = fledScene;
		this.features = features;
		this.damages = damages;
		this.otherDamages = otherDamages;
		this.insuredThirdParty = insuredThirdParty;
		this.insuredComprehensive = insuredComprehensive;
		this.physical = physical;
		this.participationProhibited = participationProhibited;
		this.criticalDefects = criticalDefects;
		this.initialImpacts = initialImpacts;
	}
	public int getVehicleId() {
		return vehicleId;
	}


	public void setVehicleId(int vehicleId) {
		this.vehicleId = vehicleId;
	}


	public String getRegistrationCountry() {
		return registrationCountry;
	}


	public void setRegistrationCountry(String registrationCountry) {
		this.registrationCountry = registrationCountry;
	}


	public String getCategory() {
		return category;
	}


	public void setCategory(String category) {
		this.category = category;
	}


	public String getClassV() {
		return classV;
	}


	public void setClassV(String classV) {
		this.classV = classV;
	}


	public String getMake() {
		return make;
	}


	public void setMake(String make) {
		this.make = make;
	}


	public String getModel() {
		return model;
	}


	public void setModel(String model) {
		this.model = model;
	}


	public int getManufactureYear() {
		return manufactureYear;
	}


	public void setManufactureYear(int manufactureYear) {
		this.manufactureYear = manufactureYear;
	}


	public String getFledScene() {
		return fledScene;
	}


	public void setFledScene(String fledScene) {
		this.fledScene = fledScene;
	}


	public String getFeatures() {
		return features;
	}


	public void setFeatures(String features) {
		this.features = features;
	}


	public String getDamages() {
		return damages;
	}


	public void setDamages(String damages) {
		this.damages = damages;
	}


	public String getOtherDamages() {
		return otherDamages;
	}


	public void setOtherDamages(String otherDamages) {
		this.otherDamages = otherDamages;
	}


	public int getInsuredThirdParty() {
		return insuredThirdParty;
	}


	public void setInsuredThirdParty(int insuredThirdParty) {
		this.insuredThirdParty = insuredThirdParty;
	}


	public int getInsuredComprehensive() {
		return insuredComprehensive;
	}


	public void setInsuredComprehensive(int insuredComprehensive) {
		this.insuredComprehensive = insuredComprehensive;
	}


	public String getPhysical() {
		return physical;
	}


	public void setPhysical(String physical) {
		this.physical = physical;
	}


	public String getParticipationProhibited() {
		return participationProhibited;
	}


	public void setParticipationProhibited(String participationProhibited) {
		this.participationProhibited = participationProhibited;
	}


	public String[] getCriticalDefects() {
		return criticalDefects;
	}


	public void setCriticalDefects(String[] criticalDefects) {
		this.criticalDefects = criticalDefects;
	}


	public String[] getInitialImpacts() {
		return initialImpacts;
	}


	public void setInitialImpacts(String[] initialImpacts) {
		this.initialImpacts = initialImpacts;
	}

	
}