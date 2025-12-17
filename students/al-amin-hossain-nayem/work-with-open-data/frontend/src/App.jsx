import { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m";
      const params = {
        format: 'JSON',
        lang: 'EN',
        geo: 'LT',
        s_adj: 'SA',
        sex: 'T',
        age: 'TOTAL',
        unit: 'PC_ACT'
      };

      try {
        const response = await fetch(`${url}?${new URLSearchParams(params)}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        const processedData = processEurostatData(jsonData, params);
        setData(processedData);
      } catch (e) {
        console.error("Error fetching or processing data: ", e);
        setError("Failed to load data. Please try again later.");
      }
    };

    fetchData();
  }, []);

  const processEurostatData = (data, fetchParams) => {
    if (!data || !data.dimension || !data.value) {
      console.error("Invalid data structure from Eurostat API");
      return [];
    }
    
    const values = data.value;
    const dimensionIds = data.id;
    const timeDimPosition = dimensionIds.indexOf('time');
    const timeCategoryIndexMap = data.dimension.time.category.index;

    const fixedDimIndicesMap = {};
    dimensionIds.forEach(dimId => {
      if (dimId !== 'time') {
        const requestedCategory = fetchParams[dimId];
        if (requestedCategory && data.dimension[dimId].category.index[requestedCategory] !== undefined) {
          fixedDimIndicesMap[dimId] = data.dimension[dimId].category.index[requestedCategory];
        } else {
          fixedDimIndicesMap[dimId] = 0;
        }
      }
    });

    const records = Object.entries(timeCategoryIndexMap).map(([dateLabel, numericalIndex]) => {
      const year = parseInt(dateLabel.split('-')[0], 10);
      if (year < 2015 || year > 2024) return null;

      let flatIndex = 0;
      let multiplier = 1;

      for (let i = dimensionIds.length - 1; i >= 0; i--) {
        const dimIdAtPos = dimensionIds[i];
        const dimSize = data.size[i];
        const idxInCurrentDim = (dimIdAtPos === 'time') ? numericalIndex : fixedDimIndicesMap[dimIdAtPos];
        
        flatIndex += idxInCurrentDim * multiplier;
        multiplier *= dimSize;
      }
      
      const value = values[flatIndex];
      return value !== undefined ? { date: dateLabel, value } : null;
    }).filter(Boolean);

    if (records.length === 0) {
      return [];
    }
    
    const yearlyData = records.reduce((acc, record) => {
        const year = record.date.substring(0, 4);
        if (!acc[year]) {
            acc[year] = { year: parseInt(year, 10), values: [] };
        }
        acc[year].values.push(record.value);
        return acc;
    }, {});

    const yearlyAvg = Object.values(yearlyData).map(d => {
        const sum = d.values.reduce((a, b) => a + b, 0);
        const avg = sum / d.values.length;
        return { year: d.year, unemployment_rate: parseFloat(avg.toFixed(2)) };
    });

    return yearlyAvg.sort((a, b) => a.year - b.year);
  };

  if (error) {
    return <div className="App"><h1>Error</h1><p>{error}</p></div>;
  }

  return (
    <div className="App">
      <h1>Lithuania Unemployment Rate (2015-2024)</h1>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="unemployment_rate" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;
