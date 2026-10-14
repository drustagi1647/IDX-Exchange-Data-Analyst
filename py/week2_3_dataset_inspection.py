import pandas as pd
import glob
import os

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
pd.set_option("display.max_rows", None)

high_missing = missing_summary[missing_summary["missing_percent"] > 90]
print("\nColumns with >90% missing values (SOLD):")
print(high_missing.sort_values("missing_percent", ascending=False))
missing_counts_listings = listings.isnull().sum()
missing_percent_listings = (missing_counts_listings / len(listings)) * 100

missing_summary_listings = pd.DataFrame({
    "missing_count": missing_counts_listings,
    "missing_percent": missing_percent_listings
})

high_missing_listings = missing_summary_listings[missing_summary_listings["missing_percent"] > 90]
print("\nColumns with >90% missing values (LISTINGS):")
print(high_missing_listings.sort_values("missing_percent", ascending=False))
numeric_cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]

print("\nNumeric distribution summary (SOLD):")
print(sold[numeric_cols].describe())
pd.set_option("display.float_format", "{:,.2f}".format)

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