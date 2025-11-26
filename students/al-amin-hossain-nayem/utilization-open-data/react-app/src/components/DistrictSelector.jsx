import React from 'react';

const DistrictSelector = ({ title, options, onSelect, selectedValue }) => {
    return (
        <div className="my-4">
            <h3 className="text-lg font-semibold mb-2">{title}</h3>
            <select
                className="w-full p-2 border border-gray-300 rounded"
                onChange={(e) => onSelect(e.target.value)}
                value={selectedValue || ''}
            >
                <option value="" disabled>Select a district</option>
                {options.map(option => (
                    <option key={option} value={option}>{option}</option>
                ))}
            </select>
        </div>
    );
};

export default DistrictSelector;
