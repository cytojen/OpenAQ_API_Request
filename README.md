# OpenAQ Weather Pollutant Dataset API

This project provides a Python script to interact with the OpenAQ API for retrieving air quality data for specified locations and parameters. The script fetches pollutant data, processes it into a user-friendly format, and exports the dataset to a CSV file.

## Features

- **Fetch location details**: Retrieve location metadata using latitude and longitude.
- **Retrieve air quality measurements**: Get historical data for multiple air quality parameters such as PM2.5, PM10, SO₂, O₃, CO, NO, NOₓ, and NO₂.
- **Data Transformation**: Processes raw data into a pivoted format with separate columns for each pollutant.
- **Export to CSV**: Saves the processed dataset as a CSV file for further analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/openaq-weather-pollutant-api.git
   cd openaq-weather-pollutant-api
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open the script `openaq_api.py` and configure the following variables:
   - `station_name`: A name to identify the monitoring station.
   - `lat`, `lon`: Latitude and longitude of the location to monitor.
   - `API_KEY`: Add your OpenAQ API key for authenticated requests.

2. Run the script:
   ```bash
   python openaq_api.py
   ```

3. The script will:
   - Fetch air quality data for the specified pollutants and date range.
   - Process and save the dataset as `station_name_air_quality_data_with_columns.csv`.

## Parameters and Customization

- **Location Radius**: Adjust the `radius` in `get_location_by_coordinates` to define the search radius for the location.
- **Pollutants**: Modify the `parameters` list to include or exclude specific pollutants.
- **Date Range**: Update the `start_date` and `end_date` variables in the `main()` function to fetch data for a custom time period.

## Example Output

The script generates a CSV file with columns for:
- Date (`date`)
- Location ID (`locationId`)
- Pollutant values (e.g., PM2.5, PM10, SO₂, etc.)
- Metadata such as `city`, `country`, `latitude`, and `longitude`.

## Limitations

- **API Rate Limits**: To respect OpenAQ's API rate limits, the script includes a 1-second delay between requests.
- **Data Availability**: Availability of pollutant data depends on OpenAQ's database for the specified location and time period.

## Dependencies

- Python 3.x
- Libraries: `requests`, `pandas`

Install dependencies using:
```bash
pip install requests pandas
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This script uses the [OpenAQ API](https://docs.openaq.org/) to retrieve air quality data.
