package com.universityProject.demo.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Setter
@Getter
public class TrafficParticipants{
	@JsonProperty("dalyvisId")
	private int participantId;
	@JsonProperty("kategorija")
	private String category;
	@JsonProperty("dalyvioTipas")
	private String participantType;
	@JsonProperty("pasisalino")
	private String fledScene;
	@JsonProperty("asmuoNezinomas")
	private String unknownPerson;
	@JsonProperty("lytis")
	private String gender;
	@JsonProperty("pilietybe")
	private String citizenship;
	@JsonProperty("amzius")
	private int age;
	@JsonProperty("neigalumas")
	private String disability;
	@JsonProperty("saugosDirzas")
	private String seatbelt;
	@JsonProperty("vaikoKedesNaudojimas")
	private String childSeatUse;
	@JsonProperty("saugosSalmoNaudojimas")
	private String helmetUse;
	@JsonProperty("oroPagalves")
	private String airbags;
	@JsonProperty("bukle")
	private String condition;
	@JsonProperty("detaliBukle")
	private String detailedCondition;
	@JsonProperty("suzalojimoMastas")
	private String injurySeverity;
	@JsonProperty("vairuotojoKvalifikacija")
	private String driverQualification;
	@JsonProperty("vairavimoStazas")
	private String driverExperience;
	@JsonProperty("busena")
	private String state;
	@JsonProperty("detaliBusena")
	private String detailedState;
	@JsonProperty("papBusena")
	private String secondaryState;
	@JsonProperty("detaliPapBusena")
	private String detailedSecondaryState;
	@JsonProperty("kaltininkas")
	private String offender;
	@JsonProperty("girtumasPromilemis")
	private double bloodAlcoholLevel;
	@JsonProperty("dalyvioBusena")
	private String participantStatus;
	@JsonProperty("teisenosStadijaBusena")
	private String legalProcessStage;
	@JsonProperty("dalyvioKetPazeidimai")
	private String[] trafficViolations;
	@JsonProperty("tpId")
	private int vehicleId;
	
	public TrafficParticipants() {
		
	}
	public TrafficParticipants(int participantId, String category, String participantType, String fledScene,
			String unknownPerson, String gender, String citizenship, int age, String disability, String seatbelt,
			String childSeatUse, String helmetUse, String airbags, String condition, String detailedCondition,
			String injurySeverity, String driverQualification, String driverExperience, String state,
			String detailedState, String secondaryState, String detailedSecondaryState, String offender,
			double bloodAlcoholLevel, String participantStatus, String legalProcessStage, String[] trafficViolations,
			int vehicleId) {
		
		this.participantId = participantId;
		this.category = category;
		this.participantType = participantType;
		this.fledScene = fledScene;
		this.unknownPerson = unknownPerson;
		this.gender = gender;
		this.citizenship = citizenship;
		this.age = age;
		this.disability = disability;
		this.seatbelt = seatbelt;
		this.childSeatUse = childSeatUse;
		this.helmetUse = helmetUse;
		this.airbags = airbags;
		this.condition = condition;
		this.detailedCondition = detailedCondition;
		this.injurySeverity = injurySeverity;
		this.driverQualification = driverQualification;
		this.driverExperience = driverExperience;
		this.state = state;
		this.detailedState = detailedState;
		this.secondaryState = secondaryState;
		this.detailedSecondaryState = detailedSecondaryState;
		this.offender = offender;
		this.bloodAlcoholLevel = bloodAlcoholLevel;
		this.participantStatus = participantStatus;
		this.legalProcessStage = legalProcessStage;
		this.trafficViolations = trafficViolations;
		this.vehicleId = vehicleId;
	}
	public int getParticipantId() {
		return participantId;
	}

	public void setParticipantId(int participantId) {
		this.participantId = participantId;
	}

	public String getCategory() {
		return category;
	}

	public void setCategory(String category) {
		this.category = category;
	}

	public String getParticipantType() {
		return participantType;
	}

	public void setParticipantType(String participantType) {
		this.participantType = participantType;
	}

	public String getFledScene() {
		return fledScene;
	}

	public void setFledScene(String fledScene) {
		this.fledScene = fledScene;
	}

	public String getUnknownPerson() {
		return unknownPerson;
	}

	public void setUnknownPerson(String unknownPerson) {
		this.unknownPerson = unknownPerson;
	}

	public String getGender() {
		return gender;
	}

	public void setGender(String gender) {
		this.gender = gender;
	}

	public String getCitizenship() {
		return citizenship;
	}

	public void setCitizenship(String citizenship) {
		this.citizenship = citizenship;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String getDisability() {
		return disability;
	}

	public void setDisability(String disability) {
		this.disability = disability;
	}

	public String getSeatbelt() {
		return seatbelt;
	}

	public void setSeatbelt(String seatbelt) {
		this.seatbelt = seatbelt;
	}

	public String getChildSeatUse() {
		return childSeatUse;
	}

	public void setChildSeatUse(String childSeatUse) {
		this.childSeatUse = childSeatUse;
	}

	public String getHelmetUse() {
		return helmetUse;
	}

	public void setHelmetUse(String helmetUse) {
		this.helmetUse = helmetUse;
	}

	public String getAirbags() {
		return airbags;
	}

	public void setAirbags(String airbags) {
		this.airbags = airbags;
	}

	public String getCondition() {
		return condition;
	}

	public void setCondition(String condition) {
		this.condition = condition;
	}

	public String getDetailedCondition() {
		return detailedCondition;
	}

	public void setDetailedCondition(String detailedCondition) {
		this.detailedCondition = detailedCondition;
	}

	public String getInjurySeverity() {
		return injurySeverity;
	}

	public void setInjurySeverity(String injurySeverity) {
		this.injurySeverity = injurySeverity;
	}

	public String getDriverQualification() {
		return driverQualification;
	}

	public void setDriverQualification(String driverQualification) {
		this.driverQualification = driverQualification;
	}

	public String getDriverExperience() {
		return driverExperience;
	}

	public void setDriverExperience(String driverExperience) {
		this.driverExperience = driverExperience;
	}

	public String getState() {
		return state;
	}

	public void setState(String state) {
		this.state = state;
	}

	public String getDetailedState() {
		return detailedState;
	}

	public void setDetailedState(String detailedState) {
		this.detailedState = detailedState;
	}

	public String getSecondaryState() {
		return secondaryState;
	}

	public void setSecondaryState(String secondaryState) {
		this.secondaryState = secondaryState;
	}

	public String getDetailedSecondaryState() {
		return detailedSecondaryState;
	}

	public void setDetailedSecondaryState(String detailedSecondaryState) {
		this.detailedSecondaryState = detailedSecondaryState;
	}

	public String getOffender() {
		return offender;
	}

	public void setOffender(String offender) {
		this.offender = offender;
	}

	public double getBloodAlcoholLevel() {
		return bloodAlcoholLevel;
	}

	public void setBloodAlcoholLevel(double bloodAlcoholLevel) {
		this.bloodAlcoholLevel = bloodAlcoholLevel;
	}

	public String getParticipantStatus() {
		return participantStatus;
	}

	public void setParticipantStatus(String participantStatus) {
		this.participantStatus = participantStatus;
	}

	public String getLegalProcessStage() {
		return legalProcessStage;
	}

	public void setLegalProcessStage(String legalProcessStage) {
		this.legalProcessStage = legalProcessStage;
	}

	public String[] getTrafficViolations() {
		return trafficViolations;
	}

	public void setTrafficViolations(String[] trafficViolations) {
		this.trafficViolations = trafficViolations;
	}

	public int getVehicleId() {
		return vehicleId;
	}

	public void setVehicleId(int vehicleId) {
		this.vehicleId = vehicleId;
	}
}