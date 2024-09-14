# DPE-TakeHomeExercise
Data Pipeline Engineer Take Home Exercise

This Python script processes Oscar-winning film data, extracts budget information, cleans and converts it to a uniform currency (USD), and enriches the dataset with additional information. It outputs the processed data into a CSV file.

## Prerequisites

Make sure you have Python 3.x installed on your machine. This script depends on several Python libraries. You can install them via `pip`.

### Installation

1. Clone the repository or download the script.
2. Install the required dependencies using the command below:

```bash
pip install -r requirements.txt
```
Required Libraries
- requests: Used for making HTTP requests to fetch data.
- pandas: A powerful library for data manipulation and analysis.
- numpy: Used for numerical operations.
- re (Regex): Used for advanced string manipulation.

To install these dependencies, add the following to a requirements.txt file:

```bash
requests
pandas
numpy
```

### How to Run

After installing the required libraries, follow these steps:

1 - Ensure the URL endpoint http://oscars.yipitdata.com/ is available and returning valid JSON data.
2 - Run the script with the following command:

```bash
python oscar.py
```

This will:

- Fetch the data from the URL.
- Extract budget information from the 'Detail URL' field.
- Convert non-USD currencies to USD using pre-defined conversion rates.
- Clean up the data, format the budget field, and output a CSV file called oscar.csv.

### Assumptions

- The URL http://oscars.yipitdata.com/ returns data in JSON format.
- The budget field may be in different currencies and formats, such as USD, GBP (£), EUR (€), or as a range.
- The conversion rates provided are for illustrative purposes and may need to be adjusted for accurate conversions.
- Budget data might not always be available, and in such cases, the missing budget is replaced by 0.

More details in EXPLAIN.md

### Output

The script will output a CSV file (oscar.csv) with the following columns:

- Film
- Producer(s)
- Production Company(s)
- Winner
- year
- year_simple
- Edition
- Budget (raw data)
- Budget_converted_to_USD (processed and converted data)
- Detail URL
- Wiki URL

### Notes

- Conversion rates may change over time. Update the conversion_rates dictionary in the script to reflect the latest rates.
- This script assumes the budgets are in common currency formats and attempts to clean them, but edge cases may require additional handling.

