import pandas as pd
import rasterio
import numpy as np
import glob
import os


# ==========================================
# 1. Load ML dataset
# ==========================================

df = pd.read_csv("data/ml_base_dataset.csv")

print("Total samples:", len(df))

# Make sure columns exist
df["Elevation_m"] = pd.to_numeric(
    df["Elevation_m"],
    errors="coerce"
)

df["Slope_degrees"] = pd.to_numeric(
    df["Slope_degrees"],
    errors="coerce"
)


# ==========================================
# 2. Find DEM files
# ==========================================

dem_files = glob.glob("data/dem*/*.tif")

print("\nDEM files:")

for file in dem_files:
    print("-", file)


# ==========================================
# 3. Process DEMs
# ==========================================

for dem_file in dem_files:

    print(
        "\nProcessing:",
        os.path.dirname(dem_file)
    )

    with rasterio.open(dem_file) as src:

        bounds = src.bounds

        # Find background points only
        indices = df.index[
            (df["Label"] == 0) &
            (df["Elevation_m"].isna()) &
            (df["Longitude"] >= bounds.left) &
            (df["Longitude"] <= bounds.right) &
            (df["Latitude"] >= bounds.bottom) &
            (df["Latitude"] <= bounds.top)
        ]

        print("Background points:", len(indices))

        for count, index in enumerate(indices):

            lon = df.at[index, "Longitude"]
            lat = df.at[index, "Latitude"]

            try:

                row, col = src.index(lon, lat)

                # Small neighborhood
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

                # ==========================================
                # Calculate local slope
                # ==========================================

                lat_rad = np.radians(lat)

                meters_lat = 111320

                meters_lon = (
                    111320 *
                    np.cos(lat_rad)
                )

                dx = src.res[0] * meters_lon
                dy = src.res[1] * meters_lat

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

                df.at[
                    index,
                    "Elevation_m"
                ] = float(center)

                df.at[
                    index,
                    "Slope_degrees"
                ] = float(slope)

            except Exception:
                continue

            if (count + 1) % 500 == 0:

                print(
                    f"Processed {count + 1}/"
                    f"{len(indices)}"
                )


# ==========================================
# 4. Save
# ==========================================

output_file = "data/ml_terrain_dataset.csv"

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 5. Report
# ==========================================

print("\n===================================")
print("BACKGROUND TERRAIN COMPLETE")
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