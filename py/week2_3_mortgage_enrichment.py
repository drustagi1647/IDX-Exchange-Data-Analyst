import pandas as pd

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

print(mortgage.head())
print(mortgage.tail())
mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)

print(mortgage_monthly.tail(12))
sold = pd.read_csv("Sold_Residential_Validated.csv", low_memory=False)
listings = pd.read_csv("Listings_Residential_Validated.csv", low_memory=False)

sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")
listings["year_month"] = pd.to_datetime(listings["ListingContractDate"]).dt.to_period("M")

print(sold[["CloseDate", "year_month"]].head())
print(listings[["ListingContractDate", "year_month"]].head())
sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listings.merge(mortgage_monthly, on="year_month", how="left")

print("\nSold rows before merge:", len(sold), "| after merge:", len(sold_with_rates))
print("Listings rows before merge:", len(listings), "| after merge:", len(listings_with_rates))

print(sold_with_rates[["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]].head())
sold_missing_rate = sold_with_rates["rate_30yr_fixed"].isnull().sum()
listings_missing_rate = listings_with_rates["rate_30yr_fixed"].isnull().sum()

print("\nSold rows with no mortgage rate:", sold_missing_rate)
print("Listings rows with no mortgage rate:", listings_missing_rate)

if sold_missing_rate == 0 and listings_missing_rate == 0:
    print("VALIDATION PASSED: every row has a mortgage rate")
else:
    print("VALIDATION FAILED: some rows have no mortgage rate, investigate before saving")
sold_with_rates.to_csv("Sold_Enriched_MortgageRates.csv", index=False)
listings_with_rates.to_csv("Listings_Enriched_MortgageRates.csv", index=False)

print("\nSaved Sold_Enriched_MortgageRates.csv and Listings_Enriched_MortgageRates.csv")