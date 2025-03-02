import json
import urllib.request
import urllib.parse
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Load CSV files
portfolio_df = pd.read_csv("dummy_portfolio_file.csv")
index_df = pd.read_csv("dummy_index_file.csv")

# Retrieve API Key from environment variables
OPENFIGI_API_KEY = os.getenv("14699768-b71a-442e-ae5a-ae81329aedd7", None)
OPENFIGI_BASE_URL = "https://api.openfigi.com"

HEADERS = {"Content-Type": "application/json"}
if OPENFIGI_API_KEY:
    HEADERS["X-OPENFIGI-APIKEY"] = OPENFIGI_API_KEY

def api_call(path: str, data: list) -> list:
    url = urllib.parse.urljoin(OPENFIGI_BASE_URL, path)
    request = urllib.request.Request(
        url=url,
        data=bytes(json.dumps(data), encoding="utf-8"),
        headers=HEADERS,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"API request failed for {data}: {e}")
        return []

def fetch_market_sectors(df: pd.DataFrame) -> dict:
    figi_list = df.iloc[:, 0].tolist()
    figi_to_sector = {}

    for figi in figi_list:
        data = [{"idType": "ID_BB_GLOBAL", "idValue": figi}]
        response = api_call("/v3/mapping", data)

        if response and isinstance(response, list) and "data" in response[0]:
            if response[0]["data"]:
                market_sector = response[0]["data"][0].get("marketSector", "Unknown")
            else:
                market_sector = "Unknown"
        else:
            market_sector = "Unknown"

        figi_to_sector[figi] = market_sector

    return figi_to_sector

# Fetch Market Sectors
portfolio_figi_to_sector = fetch_market_sectors(portfolio_df)
index_figi_to_sector = fetch_market_sectors(index_df)

portfolio_df["Market Sector"] = portfolio_df.iloc[:, 0].map(portfolio_figi_to_sector)
index_df["Market Sector"] = index_df.iloc[:, 0].map(index_figi_to_sector)

# Portfolio Exposure
total_portfolio_holding = portfolio_df["Holding"].sum()
portfolio_sector_exposure = (
    portfolio_df.groupby("Market Sector", as_index=False)["Holding"]
    .sum()
    .assign(Portfolio_Exposure=lambda df: (df["Holding"] / total_portfolio_holding) * 100)
    .drop(columns=["Holding"])
)

# Index Exposure
index_sector_exposure = (
    index_df.groupby("Market Sector", as_index=False)["Weight"]
    .sum()
    .assign(Index_Exposure=lambda df: df["Weight"] * 100)
    .drop(columns=["Weight"])
)

# Merge DataFrames 
comparison_df = pd.merge(portfolio_sector_exposure, index_sector_exposure, on="Market Sector", how="outer").fillna(0)

# Calculate the difference
comparison_df["Difference"] = comparison_df["Portfolio_Exposure"] - comparison_df["Index_Exposure"]

# Format as percentages for display
comparison_df[["Portfolio_Exposure", "Index_Exposure", "Difference"]] = (
    comparison_df[["Portfolio_Exposure", "Index_Exposure", "Difference"]].map(lambda x: f"{x:.2f}%")
)

# Print the formatted comparison DataFrame
print("\nSector Comparison:")
print(comparison_df)

# Convert percentages back to float for comparison
comparison_df["Portfolio_Exposure"] = comparison_df["Portfolio_Exposure"].str.rstrip('%').astype(float)
comparison_df["Index_Exposure"] = comparison_df["Index_Exposure"].str.rstrip('%').astype(float)
comparison_df["Difference"] = comparison_df["Difference"].str.rstrip('%').astype(float)

# Identify overweight and underweight sectors
overweight_sectors = []
underweight_sectors = []

for _, row in comparison_df.iterrows():
    sector = row["Market Sector"]
    diff = row["Difference"]

    if diff > 0:
        overweight_sectors.append(f"{sector} (+{diff:.2f}%)")
    elif diff < 0:
        underweight_sectors.append(f"{sector} ({diff:.2f}%)")

# Print Notable Differences Summary
print("\nSummary of Notable Differences")

if overweight_sectors:
    print("\n Portfolio is Overweight in:")
    for sector in overweight_sectors:
        print(f"  - {sector}")

if underweight_sectors:
    print("\n Portfolio is Underweight in:")
    for sector in underweight_sectors:
        print(f"  - {sector}")

# Plot
x_labels = comparison_df["Market Sector"]
x = np.arange(len(x_labels))
width = 0.4

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, comparison_df["Portfolio_Exposure"], width, label="Portfolio", color="#FFA500")
bars2 = ax.bar(x + width/2, comparison_df["Index_Exposure"], width, label="Index", color="#4D4D4D")

# Add data labels
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f"{height:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")

# Add labels to both bars
add_labels(bars1)
add_labels(bars2)

ax.set_xlabel("Market Sector")
ax.set_ylabel("Exposure (%)")
ax.set_title("Portfolio vs Index Exposure by Market Sector")
ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation=45, ha="right")
ax.legend()

plt.tight_layout()
plt.show()
