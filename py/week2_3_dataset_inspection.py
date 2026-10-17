# ---------------------------------------------------------------
# Weeks 2-3: Dataset structuring and validation
#
# Filtering logic: the Week 1 script already filtered both datasets
# to PropertyType == 'Residential'
# (same as sold = sold[sold.PropertyType == 'Residential']).
#   Sold:     615,707 rows -> 414,054 rows
#   Listings: 860,898 rows -> 547,162 rows
# This script loads those filtered files and validates them.
# ---------------------------------------------------------------
import pandas as pd
import glob
import os
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", "{:,.2f}".format)

sold = pd.read_csv("CombinedSold_Residential.csv", low_memory=False)
listings = pd.read_csv("CombinedListing_Residential.csv", low_memory=False)
print("SOLD dataset shape:", sold.shape)
print("LISTINGS dataset shape:", listings.shape)

print("\nSOLD columns:")
print(sold.columns.tolist())
print("\nFirst 3 rows of SOLD:")
print(sold.head(3))
missing_counts = sold.isnull().sum()
missing_percent = (missing_counts / len(sold)) * 100

missing_summary = pd.DataFrame({
    "missing_count": missing_counts,
    "missing_percent": missing_percent
})

print("\nMissing value summary (SOLD):")
print(missing_summary.sort_values("missing_percent", ascending=False))


high_missing = missing_summary[missing_summary["missing_percent"] > 90]
print("\nColumns with >90% missing values (SOLD):")
print(high_missing.sort_values("missing_percent", ascending=False))
missing_counts_listings = listings.isnull().sum()
missing_percent_listings = (missing_counts_listings / len(listings)) * 100

missing_summary_listings = pd.DataFrame({
    "missing_count": missing_counts_listings,
    "missing_percent": missing_percent_listings
})
print("\nMissing value summary (LISTINGS):")
print(missing_summary_listings.sort_values("missing_percent", ascending=False))
high_missing_listings = missing_summary_listings[missing_summary_listings["missing_percent"] > 90]
print("\nColumns with >90% missing values (LISTINGS):")
print(high_missing_listings.sort_values("missing_percent", ascending=False))
numeric_cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]

print("\nNumeric distribution summary (SOLD):")
print(sold[numeric_cols].describe())


listing_numeric_cols = ["ListPrice", "LivingArea", "DaysOnMarket"]

print("\nNumeric distribution summary (LISTINGS):")
print(listings[listing_numeric_cols].describe())
print("\nUnique PropertyType values (SOLD):", sold["PropertyType"].unique())
print("Unique PropertyType values (LISTINGS):", listings["PropertyType"].unique())
raw_sold_files = sorted(glob.glob(os.path.join("..", "csv", "CRMLSSold*.csv")))
raw_types = pd.concat(
    [pd.read_csv(f, usecols=["PropertyType"]) for f in raw_sold_files],
    ignore_index=True
)

print("\nPropertyType counts BEFORE filtering (SOLD, raw monthly files):")
print(raw_types["PropertyType"].value_counts())

print("\nPropertyType share in % (SOLD):")
print((raw_types["PropertyType"].value_counts(normalize=True) * 100).round(1))
sold.to_csv("Sold_Residential_Validated.csv", index=False)
listings.to_csv("Listings_Residential_Validated.csv", index=False)

print("\nSaved Sold_Residential_Validated.csv and Listings_Residential_Validated.csv")
print("\n--- EDA: Sold above vs. below list price ---")

price_cols = ["ListPrice", "ClosePrice"]
print("Price columns found in SOLD:", [c for c in price_cols if c in sold.columns])

print(sold[price_cols].describe())

print("Rows with ListPrice <= 0:", (sold["ListPrice"] <= 0).sum())
print("Rows with ClosePrice <= 0:", (sold["ClosePrice"] <= 0).sum())
print("Rows with ListPrice missing:", sold["ListPrice"].isnull().sum())
print("Rows with ClosePrice missing:", sold["ClosePrice"].isnull().sum())
valid = sold[(sold["ClosePrice"] > 0) & (sold["ListPrice"] > 0)]

above = (valid["ClosePrice"] > valid["ListPrice"]).sum()
below = (valid["ClosePrice"] < valid["ListPrice"]).sum()
equal = (valid["ClosePrice"] == valid["ListPrice"]).sum()
total = len(valid)

print("\nSold price vs list price (SOLD):")
print(f"Rows used: {total} (left out {len(sold) - total} with a zero or missing price)")
print(f"Sold above list: {above / total * 100:.1f}%")
print(f"Sold below list: {below / total * 100:.1f}%")
print(f"Sold exactly at list: {equal / total * 100:.1f}%")
print("\n--- EDA: Date order problems ---")

date_cols = [c for c in sold.columns if "Date" in c]
print("Date columns in SOLD:", date_cols)
dates = ["CloseDate", "ListingContractDate"]

print("\nBefore converting:")
print(sold[dates].dtypes)
print(sold[dates].head(3))
print("CloseDate blank before:", sold["CloseDate"].isnull().sum())
print("ListingContractDate blank before:", sold["ListingContractDate"].isnull().sum())

sold["CloseDate"] = pd.to_datetime(sold["CloseDate"], errors="coerce")
sold["ListingContractDate"] = pd.to_datetime(sold["ListingContractDate"], errors="coerce")

print("\nAfter converting:")
print(sold[dates].dtypes)
print("CloseDate blank after:", sold["CloseDate"].isnull().sum())
print("ListingContractDate blank after:", sold["ListingContractDate"].isnull().sum())
checkable = sold.dropna(subset=["CloseDate", "ListingContractDate"])
bad_order = checkable[checkable["CloseDate"] < checkable["ListingContractDate"]]

print("\nDate order check (SOLD):")
print(f"Rows checked: {len(checkable)} (left out {len(sold) - len(checkable)} with a blank date)")
print(f"Closed BEFORE listing date: {len(bad_order)}")
print(f"Percent of rows checked: {len(bad_order) / len(checkable) * 100:.2f}%")

print("\nExamples of rows with the problem:")
print(bad_order[["CloseDate", "ListingContractDate"]].head(5))
print("\n--- EDA: Median price by county ---")

county_cols = [c for c in sold.columns if "County" in c]
print("County columns in SOLD:", county_cols)
price_ok = sold[sold["ClosePrice"] > 0]

county_median = price_ok.groupby("CountyOrParish")["ClosePrice"].median().sort_values(ascending=False)

print("\nMedian ClosePrice by county (SOLD):")
print(f"Rows used: {len(price_ok)} (left out {len(sold) - len(price_ok)} with a zero or missing price)")
print(county_median)
print("\nTop 10 counties by median ClosePrice:")
print(county_median.head(10))
county_stats = price_ok.groupby("CountyOrParish")["ClosePrice"].agg(["count", "median"]).sort_values("median", ascending=False)

print("\nTop 10 counties by median, with number of sales:")
print(county_stats.head(10))