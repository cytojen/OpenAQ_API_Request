import requests
import pandas as pd
from datetime import datetime
import time

# OpenAQ API base URL
BASE_URL = "https://api.openaq.org/v2"

# API key
API_KEY = "faf978a47dd084bf25917b339be423e26a000bc67e35a34d53bf35c68a9c71c7"

# Headers for API requests
HEADERS = {
    "X-API-Key": API_KEY
}

# Coordinates for the monitoring station
station_name = "LLA"
lat, lon = 20.7325, -103.4343

def get_location_by_coordinates(lat, lon, radius=1000):
    """Fetch location details by coordinates."""
    url = f"{BASE_URL}/locations"
    params = {
        "limit": 1,
        "coordinates": f"{lat},{lon}",
        "radius": radius
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['meta']['found'] > 0:
            return data['results'][0]
        else:
            print(f"No location found near coordinates ({lat}, {lon}).")
            return None
    else:
        print(f"Error fetching location data: {response.status_code}")
        return None

def get_measurements(location_id, parameter, start_date, end_date):
    """Fetch measurements for a specific location and parameter."""
    url = f"{BASE_URL}/measurements"
    params = {
        "location_id": location_id,
        "parameter": parameter,
        "date_from": start_date,
        "date_to": end_date,
        "limit": 10000,
        "sort": "desc"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data['results'])
    else:
        print(f"Error fetching measurements: {response.status_code}")
        return pd.DataFrame()

def main():
    # Parameters to fetch
    parameters = ["pm25", "pm10", "so2", "o3", "co", "no", "nox", "no2"]

    # Date range
    start_date = "2024-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Processing station {station_name} at coordinates ({lat}, {lon})")

    # Fetch location details
    location = get_location_by_coordinates(lat, lon)
    if not location:
        return

    location_id = location['id']
    print(f"Found location ID: {location_id}")

    all_data = []

    for parameter in parameters:
        print(f"Fetching {parameter} data...")
        df = get_measurements(location_id, parameter, start_date, end_date)
        if not df.empty:
            df['parameter'] = parameter
            all_data.append(df)
        time.sleep(1)  # To respect API rate limits
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"Row count before pivoting: {len(combined_df)}")

        # Extract 'utc' date from the nested 'date' field and flatten 'coordinates'
        combined_df['date'] = pd.to_datetime(combined_df['date'].apply(lambda x: x['utc']))
        combined_df['latitude'] = combined_df['coordinates'].apply(lambda x: x['latitude'])
        combined_df['longitude'] = combined_df['coordinates'].apply(lambda x: x['longitude'])
        combined_df.drop(columns=['coordinates'], inplace=True)

        # Pivot the DataFrame for separate pollutant columns
        pivot_df = combined_df.pivot(
            index=['date', 'locationId', 'unit', 'city', 'country', 'latitude', 'longitude'],
            columns='parameter',
            values='value'
        ).reset_index()
        print(f"Row count after pivoting: {len(pivot_df)}")

        # Ensure all parameters are present as columns, even if no data is available
        for parameter in ["pm25", "pm10", "so2", "o3", "co", "no", "nox", "no2"]:
            if parameter not in pivot_df.columns:
                pivot_df[parameter] = None

        # Merge metadata back with the pivoted data (no duplicate columns)
        final_df = pd.merge(
            combined_df.drop(columns=['value', 'parameter']).drop_duplicates(),
            pivot_df,
            on=['date', 'locationId', 'unit', 'city', 'country', 'latitude', 'longitude'],
            how='left'
        )

        print(f"Final row count after merging: {len(final_df)}")
        # Save to CSV
        final_df.to_csv(f"{station_name}_air_quality_data_with_columns.csv", index=False)
        print(f"Data saved to {station_name}_air_quality_data_with_columns.csv")
    else:
        print(f"No data fetched for station {station_name}.")


if __name__ == "__main__":
    main()
