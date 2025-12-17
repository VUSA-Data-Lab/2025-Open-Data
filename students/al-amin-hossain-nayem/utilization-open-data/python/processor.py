def process_data(data):
    """
    Processes raw data from the World Bank API.
    - Filters out entries with null values.
    - Extracts and formats relevant fields.
    """
    if not data:
        return []

    processed_entries = []
    for entry in data:
        if entry['value'] is not None:
            processed_entries.append({
                "year": int(entry['date']),
                "value": entry['value']
            })
    
    # Sort by year
    return sorted(processed_entries, key=lambda x: x['year'], reverse=True)