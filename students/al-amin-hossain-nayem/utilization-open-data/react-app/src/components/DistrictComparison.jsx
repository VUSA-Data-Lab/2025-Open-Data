import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DistrictComparison = ({ data1, data2 }) => {
    if (!data1 && !data2) {
        return <div className="text-center p-4">Enter a district/city name to see comparison. For example: Dhaka, Vilnius</div>;
    }

    const chartData = [
        {
            name: 'Population',
            [data1?.name]: data1?.data.population,
            [data2?.name]: data2?.data.population,
        },
        {
            name: 'Education Rate (%)',
            [data1?.name]: data1?.data.education_rate,
            [data2?.name]: data2?.data.education_rate,
        },
    ];

    return (
        <div className="my-8">
            <h2 className="text-2xl font-bold text-center mb-4">District/City Comparison</h2>
            
            <div className="overflow-x-auto mb-8">
                <table className="min-w-full bg-white border border-gray-200">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="py-2 px-4 border-b">Metric</th>
                            <th className="py-2 px-4 border-b">{data1 ? data1.name : 'District 1'}</th>
                            <th className="py-2 px-4 border-b">{data2 ? data2.name : 'District 2'}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td className="py-2 px-4 border-b font-semibold">Population</td>
                            <td className="py-2 px-4 border-b">{data1 ? data1.data.population.toLocaleString() : 'N/A'}</td>
                            <td className="py-2 px-4 border-b">{data2 ? data2.data.population.toLocaleString() : 'N/A'}</td>
                        </tr>
                        <tr>
                            <td className="py-2 px-4 border-b font-semibold">Education Rate (%)</td>
                            <td className="py-2 px-4 border-b">{data1 ? data1.data.education_rate : 'N/A'}</td>
                            <td className="py-2 px-4 border-b">{data2 ? data2.data.education_rate : 'N/A'}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {data1 && <Bar dataKey={data1.name} fill="#8884d8" />}
                    {data2 && <Bar dataKey={data2.name} fill="#82ca9d" />}
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default DistrictComparison;
