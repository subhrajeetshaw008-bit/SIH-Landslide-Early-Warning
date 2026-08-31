import pandas as pd
import rasterio
import numpy as np
import glob
import os


input_file = "data/ml_terrain_dataset.csv"
output_file = "data/ml_terrain_dataset_final.csv"

df = pd.read_csv(input_file)

# Only points that still need terrain
missing = df[
    df["Elevation_m"].isna()
].index

print("Points needing terrain:", len(missing))

dem_files = glob.glob("data/dem*/*.tif")

for dem_file in dem_files:

    print("\nProcessing:", dem_file)

    with rasterio.open(dem_file) as src:

        bounds = src.bounds

        indices = [
            i for i in missing
            if (
                bounds.left <= df.at[i, "Longitude"] <= bounds.right
                and
                bounds.bottom <= df.at[i, "Latitude"] <= bounds.top
            )
        ]

        print("Points in DEM:", len(indices))

        for i in indices:

            lon = df.at[i, "Longitude"]
            lat = df.at[i, "Latitude"]

            try:

                row, col = src.index(lon, lat)

                window = rasterio.windows.Window(
                    col - 1,
                    row - 1,
                    3,
                    3
                )

                elevation = src.read(
                    1,
                    window=window,
                    boundless=True,
                    fill_value=np.nan
                ).astype(float)

                if src.nodata is not None:
                    elevation[
                        elevation == src.nodata
                    ] = np.nan

                center = elevation[1, 1]

                if not np.isfinite(center):
                    continue

                lat_rad = np.radians(lat)

                dx = (
                    src.res[0]
                    * 111320
                    * np.cos(lat_rad)
                )

                dy = src.res[1] * 111320

                gy, gx = np.gradient(
                    elevation,
                    dy,
                    dx
                )

                slope = np.degrees(
                    np.arctan(
                        np.sqrt(
                            gx[1, 1] ** 2 +
                            gy[1, 1] ** 2
                        )
                    )
                )

                if np.isfinite(slope):

                    df.at[i, "Elevation_m"] = float(center)
                    df.at[i, "Slope_degrees"] = float(slope)

            except Exception:
                continue

# Save
df.to_csv(
    output_file,
    index=False
)

print("\n===================================")
print("FINAL TERRAIN DATASET")
print("===================================")

print("Total samples:", len(df))
print(
    "Elevation missing:",
    df["Elevation_m"].isna().sum()
)
print(
    "Slope missing:",
    df["Slope_degrees"].isna().sum()
)

print("\nLabels:")
print(df["Label"].value_counts())

print("\nSaved to:")
print(output_file)