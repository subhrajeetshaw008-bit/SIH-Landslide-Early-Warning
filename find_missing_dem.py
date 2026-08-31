import pandas as pd
import rasterio
import glob

df = pd.read_csv("data/ner_landslides.csv")

dem_files = glob.glob("data/**/*.tif", recursive=True)

covered = pd.Series(False, index=df.index)

for dem_file in dem_files:
    with rasterio.open(dem_file) as src:
        b = src.bounds

        inside = (
            (df["Longitude"] >= b.left) &
            (df["Longitude"] <= b.right) &
            (df["Latitude"] >= b.bottom) &
            (df["Latitude"] <= b.top)
        )

        covered = covered | inside

missing = df[~covered].copy()

print("Total landslides:", len(df))
print("Covered:", covered.sum())
print("Missing:", len(missing))

print("\nMissing-location range:")
print("Latitude:", missing["Latitude"].min(), "to", missing["Latitude"].max())
print("Longitude:", missing["Longitude"].min(), "to", missing["Longitude"].max())

print("\nMissing landslides by state:")
print(missing["State"].value_counts().to_string())

missing.to_csv(
    "data/ner_missing_dem_points.csv",
    index=False
)

print("\nSaved:")
print("data/ner_missing_dem_points.csv")