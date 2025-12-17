import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CountryChart = ({ data, title }) => {
    return (
        <div className="my-8">
            <h2 className="text-2xl font-bold text-center mb-4">{title}</h2>
            <ResponsiveContainer width="100%" height={400}>
                <BarChart
                    data={data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="bangladesh" fill="#8884d8" name="Bangladesh" />
                    <Bar dataKey="lithuania" fill="#82ca9d" name="Lithuania" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default CountryChart;
