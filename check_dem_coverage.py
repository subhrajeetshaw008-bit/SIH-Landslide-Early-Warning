import pandas as pd
import rasterio
import glob
import os

# Load landslide points
df = pd.read_csv("data/ner_landslides.csv")

# Find all DEM files
dem_files = glob.glob("data/**/*.tif", recursive=True)

print(f"Found {len(dem_files)} DEM file(s)\n")

covered = pd.Series(False, index=df.index)

for dem_file in dem_files:

    print("Checking:", os.path.basename(dem_file))

    with rasterio.open(dem_file) as src:

        bounds = src.bounds

        inside = (
            (df["Longitude"] >= bounds.left) &
            (df["Longitude"] <= bounds.right) &
            (df["Latitude"] >= bounds.bottom) &
            (df["Latitude"] <= bounds.top)
        )

        covered = covered | inside

        print(f"Points covered by this DEM: {inside.sum()}")
        print("Bounds:", bounds)
        print()

print("==============================")
print("TOTAL COVERAGE")
print("==============================")

print("Total landslides:", len(df))
print("Covered:", covered.sum())
print("Missing:", (~covered).sum())

print(
    "Coverage percentage:",
    round(covered.mean() * 100, 2),
    "%"
)