package com.universityProject.demo.service;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Service;


import com.universityProject.demo.model.EuroService;

@Service
public class CsvReaderService{

	public Map<String,EuroService> readCsvFile(String filePath) throws IOException{
		List<EuroService> dataList = new ArrayList<>();
		Map<String,EuroService> topLow = new HashMap<>();
		try(Reader reader = new FileReader(filePath)){
			CSVParser csvParser = new CSVParser(reader,CSVFormat.DEFAULT.withFirstRecordAsHeader().withIgnoreHeaderCase().withTrim());
			for(CSVRecord csvRecord : csvParser) {
				EuroService euroS = new EuroService();
				euroS.setGeo(csvRecord.get("geo"));
				euroS.setPurchases(csvRecord.get("purchase"));
				euroS.setTime(csvRecord.get("TIME_PERIOD"));
				euroS.setTimeFrequency(csvRecord.get("freq"));
				euroS.setUnitMeasure(csvRecord.get("unit"));
				euroS.setValue(Double.parseDouble(csvRecord.get("OBS_VALUE")));
				dataList.add(euroS);
				
			}
			for(int i=0;i<dataList.size();i++) {
				for(int j=i+1; i<dataList.size();i++) {
					if(dataList.get(i).getValue()>dataList.get(j).getValue()) {
						topLow.put(dataList.get(j).getGeo(), dataList.get(j));
					}else {
						topLow.put(dataList.get(i).getGeo(), dataList.get(i));
					}
				}
			}
		}
		return topLow;
	}
}