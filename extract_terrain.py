import pandas as pd
import rasterio
import glob
import os


# ==========================================
# 1. Load GSI NER landslide dataset
# ==========================================

input_file = "data/ner_landslides.csv"

df = pd.read_csv(input_file)

print("Loaded landslide records:", len(df))


# ==========================================
# 2. Find all DEM files
# ==========================================

dem_files = glob.glob(
    "data/dem*/*.tif"
)

print("\nDEM files found:")

for file in dem_files:
    print("-", file)


# ==========================================
# 3. Create elevation column
# ==========================================

df["Elevation_m"] = None


# ==========================================
# 4. Extract elevation
# ==========================================

for dem_file in dem_files:

    print("\nProcessing:", os.path.basename(os.path.dirname(dem_file)))

    with rasterio.open(dem_file) as src:

        bounds = src.bounds

        print("Bounds:", bounds)

        for index, row in df.iterrows():

            # Skip if elevation already found
            if pd.notna(df.at[index, "Elevation_m"]):
                continue

            longitude = row["Longitude"]
            latitude = row["Latitude"]

            # Check whether point is inside DEM
            if (
                bounds.left <= longitude <= bounds.right
                and
                bounds.bottom <= latitude <= bounds.top
            ):

                try:

                    value = next(
                        src.sample(
                            [(longitude, latitude)]
                        )
                    )[0]

                    # Ignore invalid raster values
                    if value != src.nodata:

                        df.at[index, "Elevation_m"] = float(value)

                except Exception:
                    pass


# ==========================================
# 5. Convert elevation to numeric
# ==========================================

df["Elevation_m"] = pd.to_numeric(
    df["Elevation_m"],
    errors="coerce"
)


# ==========================================
# 6. Save result
# ==========================================

output_file = "data/ner_terrain_features.csv"

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 7. Report results
# ==========================================

total = len(df)

found = df["Elevation_m"].notna().sum()

missing = total - found

print("\n===================================")
print("TERRAIN EXTRACTION COMPLETE")
print("===================================")

print("Total landslides:", total)
print("Elevation found:", found)
print("Elevation missing:", missing)

print(
    "Coverage:",
    round(found / total * 100, 2),
    "%"
)

print("\nElevation statistics:")

print(
    df["Elevation_m"].describe()
)

print("\nSaved to:")
print(output_file)