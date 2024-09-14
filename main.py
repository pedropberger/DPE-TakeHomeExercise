import requests
import pandas as pd
import numpy as np
import re


# URL to fetch data
url = "http://oscars.yipitdata.com/"

# Fetch data from URL
response = requests.get(url)
data = response.json()

# Use json_normalize to flatten the JSON structure
oscar = pd.json_normalize(data['results'], 'films', ['year'])


def fetch_budget(url):
    try:
        # Get the JSON content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Load the JSON data
        data = response.json()
        
        # Extract the 'Budget' field
        budget = data.get("Budget", None)  # Returns None if 'Budget' is not found
        return budget
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def add_budget_column(df):
    # Apply the fetch_budget function to each row of the 'Detail URL' column
    df['Budget'] = df['Detail URL'].apply(fetch_budget)
    return df

oscar = add_budget_column(oscar)
# The 'oscar' dataframe will now have a new 'Budget' column with the extracted data


# Conversion rates (example values, adjust if necessary)
conversion_rates = {
    '£': 1.35,   # Example: 1 GBP = 1.35 USD
    '€': 1.18,   # Example: 1 EUR = 1.18 USD
    '₤': 1.35    # Treating '₤' as GBP for now
}

# Removes all characters from 'or' including itself in the specified column, and create a temporary column to work with
oscar['Budget_aux'] = oscar['Budget'].str.split('or', expand = True)[0]

# Helper function to convert non-USD values to USD
def convert_to_usd(amount, currency_symbol):
    if currency_symbol in conversion_rates:
        return amount * conversion_rates[currency_symbol]
    return amount

# Helper function to clean up budget
def clean_budget(budget):
    if pd.isna(budget):  # If NaN, return 0
        return 0

    # Remove unnecessary symbols like brackets, estimations, etc.
    budget = re.sub(r'\[.*?\]', '', str(budget)).strip()
    budget = re.sub(r'\(.*?\)', '', budget).strip()

    # Handle ranges (e.g., "$1.2 million - $2.275 million")
    if '–' in budget or '-' in budget:
        budget_parts = budget.split('–')[0].split('-')[0].strip()
        if 'million' in budget.lower():
            budget = budget_parts + ' million'
        else:
            budget = budget_parts


    # Identify the currency symbol and value
    currency_symbol = None
    if budget.startswith('US$') or budget.startswith('$'):
        currency_symbol = '$'
        budget = budget.replace('US$', '').replace('$', '').strip()
    elif budget.startswith('£'):
        currency_symbol = '£'
        budget = budget.replace('£', '').strip()
    elif budget.startswith('€'):
        currency_symbol = '€'
        budget = budget.replace('€', '').strip()
    elif budget.startswith('₤'):
        currency_symbol = '₤'
        budget = budget.replace('₤', '').strip()

    # Handle values like "million" or "billion"
    if 'million' in budget.lower():
        budget_value = float(re.sub(r'[^\d.]', '', budget)) * 1_000_000
    elif 'billion' in budget.lower():
        budget_value = float(re.sub(r'[^\d.]', '', budget)) * 1_000_000_000
    else:
        budget_value = float(re.sub(r'[^\d]', '', budget))  # Remove non-numeric characters

    # Convert to USD if necessary
    if currency_symbol and currency_symbol != '$':
        budget_value = convert_to_usd(budget_value, currency_symbol)

    return int(budget_value)


# Apply cleaning function to 'Budget' column
oscar['Budget_converted_to_USD'] = oscar['Budget_aux'].apply(clean_budget)

# Drop auxiliar columns
oscar.drop('Budget_aux', axis=1, inplace=True)


# Function to extract 'year_simple' and 'edition'
def clean_year_column(row):
    # Extract the year part (e.g., '1927 / 28' -> '1927', '1928', etc.)
    year_match = re.search(r'(\d{4})', row)
    year_simple = year_match.group(1) if year_match else None
    
    # Extract the edition number (e.g., '(1st)', '(2nd)', etc.)
    edition_match = re.search(r'\((\d+)(?:st|nd|rd|th)\)', row)
    edition = edition_match.group(1) if edition_match else None
    
    return pd.Series([year_simple, edition])

# Apply the function to the 'year' column
oscar[['year_simple', 'Edition']] = oscar['year'].apply(clean_year_column)

# Reordering for a more intuitive order IMO
new_order = ['Film','Producer(s)','Production Company(s)','Winner','year','year_simple','Edition','Budget','Budget_converted_to_USD', 'Detail URL','Wiki URL']
oscar = oscar[new_order]

#Exporting CSV
oscar.to_csv('output/oscar.csv')