import React, { useEffect, useState } from 'react';
import { loadData } from '../utils/dataLoader';
import CountryChart from '../components/CountryChart';
import DistrictSelector from '../components/DistrictSelector';
import DistrictComparison from '../components/DistrictComparison';

const Home = () => {
    const [fullData, setFullData] = useState(null);
    const [populationData, setPopulationData] = useState([]);
    const [educationData, setEducationData] = useState([]);
    const [bdDistrictOptions, setBdDistrictOptions] = useState([]);
    const [ltDistrictOptions, setLtDistrictOptions] = useState([]);
    const [selectedDistrict1, setSelectedDistrict1] = useState(null);
    const [selectedDistrict2, setSelectedDistrict2] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const result = await loadData();
            if (result) {
                setFullData(result);
                setPopulationData(transformData(result.population));
                
                // Create separate lists of district names for the dropdowns
                const bdDistricts = result.districts.bangladesh.map(d => d.name).sort();
                const ltDistricts = result.districts.lithuania.map(d => d.name).sort();
                setBdDistrictOptions(bdDistricts);
                setLtDistrictOptions(ltDistricts);

                // Filter for primary school enrollment
                const primaryEnrollment = {
                    bangladesh: result.education.bangladesh.filter(item => item.indicator === 'SE.PRM.ENRR'),
                    lithuania: result.education.lithuania.filter(item => item.indicator === 'SE.PRM.ENRR')
                };
                setEducationData(transformData(primaryEnrollment));
            }
        };

        fetchData();
    }, []);

    // Transforms data to be suitable for Recharts
    const transformData = (data) => {
        if (!data || !data.bangladesh || !data.lithuania) {
            return [];
        }
    
        const combined = {};
    
        data.bangladesh.forEach(item => {
            if (!combined[item.year]) {
                combined[item.year] = { year: item.year };
            }
            combined[item.year].bangladesh = item.value;
        });
    
        data.lithuania.forEach(item => {
            if (!combined[item.year]) {
                combined[item.year] = { year: item.year };
            }
            combined[item.year].lithuania = item.value;
        });
    
        // Fill in missing values for either country with null
        Object.keys(combined).forEach(year => {
            if (combined[year].bangladesh === undefined) {
                combined[year].bangladesh = null;
            }
            if (combined[year].lithuania === undefined) {
                combined[year].lithuania = null;
            }
        });
    
        return Object.values(combined).sort((a, b) => b.year - a.year);
    };

    const findDistrictData = (name, country) => {
        if (!name || !fullData) return null;
        const district = fullData.districts[country].find(d => d.name === name);
        return district ? { name, data: district } : null;
    }

    const handleSelect1 = (name) => {
        setSelectedDistrict1(findDistrictData(name, 'bangladesh'));
    };

    const handleSelect2 = (name) => {
        setSelectedDistrict2(findDistrictData(name, 'lithuania'));
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-center my-4">World Bank Data Comparison</h1>
            <p className='text-xl font-bold text-center my-4'>Bangladesh vs Lithuania</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <DistrictSelector title="Bangladesh Districts" options={bdDistrictOptions} onSelect={handleSelect1} selectedValue={selectedDistrict1?.name} />
                <DistrictSelector title="Lithuania Districts" options={ltDistrictOptions} onSelect={handleSelect2} selectedValue={selectedDistrict2?.name} />
            </div>

            {(selectedDistrict1 || selectedDistrict2) && <DistrictComparison data1={selectedDistrict1} data2={selectedDistrict2} />}

            {populationData.length > 0 ? (
                <div>
                    <CountryChart data={populationData} title="Population" />
                    <CountryChart data={educationData} title="Primary School Enrollment" />
                </div>
            ) : (
                <p className="text-center">Loading data...</p>
            )}
        </div>
    );
};

export default Home;
