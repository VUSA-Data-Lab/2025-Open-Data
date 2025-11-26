import pandas as pd
import requests
import json
import os

def fetch_data():
    """
    Fetches monthly unemployment data for Lithuania from Eurostat.
    """
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m"
    params = {
        'format': 'JSON',
        'lang': 'EN',
        'geo': 'LT',
        's_adj': 'SA',  # Seasonally adjusted
        'sex': 'T',     # Total
        'age': 'TOTAL', # Total
        'unit': 'PC_ACT' # Percentage of active population
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data = response.json()
        return json_data, params
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

def process_data(data, fetch_params):
    """
    Processes the raw Eurostat data to calculate the average yearly unemployment rate for 2015-2024.
    """
    if not data:
        return None

    values = data.get('value', {})
    
    # Get dimension information
    dimension_ids = data['id'] # 'id' is at the top level
    
    # Get the position of 'time' dimension
    time_dim_position = dimension_ids.index('time')
    
    # Get the category indices for all dimensions that are *not* time.
    fixed_dim_indices_map = {}
    for dim_id in dimension_ids:
        if dim_id != 'time':
            requested_category = fetch_params.get(dim_id)
            if requested_category:
                # Use the category index from the fetched data's dimension structure
                fixed_dim_indices_map[dim_id] = data['dimension'][dim_id]['category']['index'][requested_category]
            else:
                fixed_dim_indices_map[dim_id] = 0 # Default to 0 for robustness

    
    time_category_index_map = data['dimension']['time']['category']['index'] # Maps date_str to numerical_index (int)

    records = []
    
    for date_label, numerical_index in time_category_index_map.items():
        year = int(date_label.split('-')[0])
        if not (2015 <= year <= 2024):
            continue 

        current_dim_indices = []
        for dim_id in dimension_ids:
            if dim_id == 'time':
                current_dim_indices.append(numerical_index)
            else:
                current_dim_indices.append(fixed_dim_indices_map[dim_id])

        # Calculate the flat index from multi-dimensional indices
        # The order of dimensions is given by dimension_ids
        flat_index = 0
        multiplier = 1
        
        # Iterate dimensions in reverse order to correctly calculate the flat index
        for i in range(len(dimension_ids) -1, -1, -1):
            dim_id_at_pos = dimension_ids[i]
            dim_size = data['size'][i] # size of the current dimension
            
            if dim_id_at_pos == 'time':
                idx_in_current_dim = numerical_index
            else:
                idx_in_current_dim = fixed_dim_indices_map[dim_id_at_pos]

            flat_index += idx_in_current_dim * multiplier
            multiplier *= dim_size

        value_key = str(flat_index) # The keys in values are strings of flat indices
        
        value = values.get(value_key)
        
        if value is not None:
            records.append({'date': date_label, 'value': value})

    if not records:
        print("No data found for the specified period or all values are missing.")
        return None

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Compute yearly average
    yearly_avg = df.resample('YE').mean()
    yearly_avg['year'] = yearly_avg.index.year
    
    # Format for JSON
    result = yearly_avg[['year', 'value']].to_dict(orient='records')
    for record in result:
        record['value'] = round(record['value'], 2)

    return result

def main():
    """
    Main function to fetch, process, and save the data.
    """
    data, params = fetch_data()
    processed_data = process_data(data, params)
    
    if processed_data:
        # Save to processed.json in the root directory
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'processed.json')
        with open(output_path, 'w') as f:
            json.dump(processed_data, f, indent=4)
        print(f"Data successfully processed and saved to {output_path}")

if __name__ == "__main__":
    main()