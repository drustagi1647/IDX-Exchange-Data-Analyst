import glob
import os
import pandas as pd

CSV_FOLDER = os.path.join("..", "csv")

sold_files = sorted(glob.glob(os.path.join(CSV_FOLDER, "CRMLSSold*.csv")))
listing_files = sorted(glob.glob(os.path.join(CSV_FOLDER, "CRMLSListing*.csv")))
print(f"Found {len(sold_files)} sold files")
print(f"Found {len(listing_files)} listing files")
sold_frames = []
for f in sold_files:
    df = pd.read_csv(f, low_memory=False)
    print(f"{f}: {len(df)} rows")
    sold_frames.append(df)

listing_frames = []
for f in listing_files:
    df = pd.read_csv(f, low_memory=False)
    print(f"{f}: {len(df)} rows")
    listing_frames.append(df)

sold = pd.concat(sold_frames, ignore_index=True)
listings = pd.concat(listing_frames, ignore_index=True)

print(f"Combined sold rows: {len(sold)}")
print(f"Combined listing rows: {len(listings)}")
sold_residential = sold[sold["PropertyType"] == "Residential"]
listings_residential = listings[listings["PropertyType"] == "Residential"]

print(f"Sold residential rows: {len(sold_residential)}")
print(f"Listing residential rows: {len(listings_residential)}")
sold_residential.to_csv("CombinedSold_Residential.csv", index=False)
listings_residential.to_csv("CombinedListing_Residential.csv", index=False)

print("Saved CombinedSold_Residential.csv and CombinedListing_Residential.csv")