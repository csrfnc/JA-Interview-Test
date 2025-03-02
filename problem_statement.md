# Introduction


In this task, you will be working with two CSV files containing portfolio and index data. Your goal is to analyze and compare the portfolio against the index based on Market Sector. This involves reading the data, enriching it with additional information from an external API, grouping and comparing the data, and finally visualizing the results.

During the interview are expected to:
1. Have completed all 4 steps bellow prior to the interview.
2. Explain your code and be able to answer any questions during the interview.

## Requirements


You will be provided with two files:

- `dummy_portfolio_file.csv`
- `dummy_index_file.csv`

You will need Python and pip installed. Additionally, you will need the following Python packages in your environment:

- pandas
- matplotlib
- requests
- urllib

You'll be making API calls to the OpenFIGI API, so refer to the documentation and GitHub example for guidance:

- [API Documentation](https://www.openfigi.com/api)
- [GitHub API Request Example](https://github.com/OpenFIGI/api-examples/blob/main/python/example.py)

## The Task

Your task is to produce analytics to compare the portfolio against the index file based on Market Sector.

### Step 1: Data Input

Using the Python package pandas, read the files into memory:

**Portfolio CSV** (`dummy_portfolio_file.csv`)
```sql
FIGI STRING -- Security Identifier
Ticker STRING -- Parent Company
Code STRING -- Product Code of the portfolio
Holding FLOAT -- The total amount held of the security within the portfolio
```

Index CSV (`dummy_index_file.csv`)
```sql
FIGI STRING -- Security Identifier
Ticker STRING -- Parent Company
Code STRING -- Product Code of the index
Weight FLOAT -- The total amount held of the security within the index
```

Keep in mind of error handling and file path management.

### Step 2: Data Enrichment via OpenFIGI API

Using the [GitHub API Request Example](https://github.com/OpenFIGI/api-examples/blob/main/python/example.py) example, enrich the dataframes with `Market Sector` information:

For each FIGI in both dataframes, make an API request to retrieve the Market Sector from OpenFIGI.

Consider the following:
- Parse JSON responses to capture the required fields.
- Handle errors gracefully if no data is returned.
- Merge the additional fields back into the original dataframes.

### Step 3: Grouping and Comparison by Market Sector

Group both dataframes by Market Sector.

**Portfolio Exposure:**

Sum weighted holdings per sector (i.e., WEIGHT = HOLDING / SUM(HOLDING)).
Convert holding sums to percentages of the total.

**Index Exposure:**
- Sum weights per sector.
- Convert weights to percentages of the total index weight.
- Compare sector exposures and highlight notable differences.

### Step 4: Visualization
Create a grouped bar chart using matplotlib:

- X-axis: Market Sectors
- Y-axis: Percentage Exposure
- Two bars per sector (Portfolio vs. Index)
- Include a legend and title for clarity.

# Sample Data Tables:

### Portfolio (`dummy_portfolio_file.csv`)
| FIGI      | Holding |
|-----------|---------|
| BBG000A1  | 150     |
| BBG000B2  | 200     |
| BBG000C3  | 100     |
| BBG000D4  | 250     |
| BBG000E5  | 180     |
| BBG000F6  | 120     |
**Total Holdings** = 150 + 200 + 100 + 250 + 180 + 120 = **1000**
---
### Index (`dummy_index_file.csv`)
| FIGI      | Weight (%) |
|-----------|------------|
| BBG000A1  | 0.2        |
| BBG000C3  | 0.15       |
| BBG000D4  | 0.25       |
| BBG000B2  | 0.10       |
| BBG000E5  | 0.20       |
| BBG000F6  | 0.10       |
**Total Weight** = 20 + 15 + 25 + 10 + 20 + 10 = **100%**


After calling the API, we enrich our data with the corresponding Ticker and Market Sector.
### Enriched Portfolio DataFrame
| FIGI      | Holding | Ticker | Market Sector |
|-----------|---------|--------|---------------|
| BBG000A1  | 150     | ABC    | Equity    |
| BBG000B2  | 200     | DEF    | Corporate    |
| BBG000C3  | 100     | GHI    | Currency    |
| BBG000D4  | 250     | JKL    | Equity    |
| BBG000E5  | 180     | MNO    | Government        |
| BBG000F6  | 120     | PQR    | Corporate    |
### Enriched Index DataFrame
| FIGI      | Weight (%) | Ticker | Market Sector |
|-----------|------------|--------|---------------|
| BBG000A1  | 20         | ABC    | Equity    |
| BBG000C3  | 15         | GHI    | Currency    |
| BBG000D4  | 25         | JKL    | Equity    |
| BBG000B2  | 10         | DEF    | Corporate    |
| BBG000E5  | 20         | MNO    | Government        |
| BBG000F6  | 10         | PQR    | Corporate    |

### For the Portfolio
Group by **Market Sector** and sum the holdings:

**Equity:**
 - Holdings: 150 (BBG000A1) + 250 (BBG000D4) = **400**  
 - Percentage Exposure = (400 / 1000) × 100 = **40%**

**Corporate:**  
 - Holdings: 200 (BBG000B2) + 120 (BBG000F6) = **320**  
 - Percentage Exposure = (320 / 1000) × 100 = **32%**

**Currency:**  
 - Holding: 100 (BBG000C3) = **100**  
 - Percentage Exposure = (100 / 1000) × 100 = **10%**

**Government:**  
 - Holding: 180 (BBG000E5) = **180**  
 - Percentage Exposure = (180 / 1000) × 100 = **18%**

### For the Index
Group by **Market Sector** and sum the weights:

**Equity:**  
 - Weights: 20 (BBG000A1) + 25 (BBG000D4) = **45%**  
 - Percentage Exposure = **45%**

**Currency:**  
 - Weight: 15 (BBG000C3) = **15%**  
 - Percentage Exposure = **15%**

**Corporate:**  
 - Weights: 10 (BBG000B2) + 10 (BBG000F6) = **20%**  
 - Percentage Exposure = **20%**

**Government:**  
 - Weight: 20 (BBG000E5) = **20%**  
 - Percentage Exposure = **20%**
---

