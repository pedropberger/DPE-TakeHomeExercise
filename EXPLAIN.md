# Explanation of Data Handling and Processing Decisions

This file outlines some key considerations and decisions made during the processing of the Oscar-winning films dataset, particularly regarding the handling of fields such as the `Winner` column, movie information URLs, currency conversions, and year data.

## 1. Handling of the `Winner` Field

The original dataset included a `Winner` field that was inconsistently formatted, containing both `True/False` values and `1/0` values to indicate whether a film won an Oscar. When using a Pandas DataFrame, the library automatically converted all values in the `Winner` column to `True/False`, ensuring consistency in the dataset. This behavior simplified the data processing, and no further conversions were necessary.

## 2. Missing Movie Information URLs

Several URLs intended to provide detailed movie information were unavailable during the data fetching process. These URLs, listed below, returned errors or were not accessible:

- `http://oscars.yipitdata.com/films/Les_Mis%C3%A9rables_(1935_film)`
- `http://oscars.yipitdata.com/films/Who%2527s_Afraid_of_Virginia_Woolf%3F_(film)`
- `http://oscars.yipitdata.com/films/Secrets_%26_Lies_(film)`
- `http://oscars.yipitdata.com/films/Les_Mis%C3%A9rables_(2012_film)`

Since the necessary information could not be retrieved from these URLs, any related fields, such as `Budget`, were left empty and turn in zero later.

## 3. Hypothetical Conversion Rates

In the dataset, some budget values were presented in different currencies (USD, GBP, EUR, etc.). To standardize the budgets, I applied hypothetical conversion rates for each currency. These rates were used purely for the purpose of this exercise and should **not** be considered accurate for production use.

The conversion rates I used are as follows:
- GBP (£) to USD: 1.35
- EUR (€) to USD: 1.18
- ₤ (treated as GBP): 1.35

For production environments, it is recommended to fetch the latest conversion rates from a reliable financial data source or API.

## 4. Handling of Multiple Currency Values

In some cases, the `Budget` field contained values in multiple currencies, such as "$1 million or £467,000". The word "or" was used instead of a dash to indicate alternative values, not a range.

To ensure consistency, I chose the **first** value presented in this cases. For instance, if the field read "$1 million or £467,000", I selected the $1 million value.

## 5. Cleaning of the `year` Field

The raw `year` data included both the year of the film’s release and the edition of the Oscars in a combined format (e.g., `1927 / 28 (1st)`).

From this data:
- I created a clean `year_simple` column by extracting only the **first year** listed for each film (e.g., `1927`).
- I also created an `Edition` column to store the Oscar edition (e.g., `1st`, `2nd`, etc.) because I thought this information could be useful and it was already present in the dataset.

## Conclusion

These decisions were made to standardize and simplify the dataset, making it easier to work with in downstream tasks. Any modifications or adjustments, particularly regarding the use of conversion rates or unavailable URLs, should be made based on the specific needs of the project or the production environment.
