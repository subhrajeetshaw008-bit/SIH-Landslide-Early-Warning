import pandas as pd
import rasterio
import numpy as np
import glob
import os


# ==========================================
# 1. Load landslide dataset
# ==========================================

input_file = "data/ner_terrain_features.csv"

df = pd.read_csv(input_file)

print("Loaded landslide records:", len(df))


# ==========================================
# 2. Find DEM files
# ==========================================

dem_files = glob.glob("data/dem*/*.tif")

print("\nDEM files found:")

for file in dem_files:
    print("-", file)


# ==========================================
# 3. Create slope column
# ==========================================

df["Slope_degrees"] = np.nan


# ==========================================
# 4. Process each DEM
# ==========================================

for dem_file in dem_files:

    print(
        "\nProcessing:",
        os.path.basename(os.path.dirname(dem_file))
    )

    with rasterio.open(dem_file) as src:

        bounds = src.bounds

        # Find points inside this DEM
        inside_indices = df.index[
            (df["Longitude"] >= bounds.left) &
            (df["Longitude"] <= bounds.right) &
            (df["Latitude"] >= bounds.bottom) &
            (df["Latitude"] <= bounds.top) &
            (df["Slope_degrees"].isna())
        ]

        print(
            "Points to process:",
            len(inside_indices)
        )

        if len(inside_indices) == 0:
            continue

        # ==========================================
        # Process each point using a small 3x3 window
        # ==========================================

        for count, index in enumerate(inside_indices):

            longitude = df.at[index, "Longitude"]
            latitude = df.at[index, "Latitude"]

            try:

                # Get raster row/column
                row, col = src.index(
                    longitude,
                    latitude
                )

                # Read only a 3x3 neighborhood
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

                # Replace nodata
                if src.nodata is not None:
                    elevation[
                        elevation == src.nodata
                    ] = np.nan

                # Need at least some valid elevation values
                if np.all(np.isnan(elevation)):
                    continue

                # ==========================================
                # Calculate local slope
                # ==========================================

                latitude_rad = np.radians(latitude)

                meters_per_degree_lat = 111320

                meters_per_degree_lon = (
                    111320 *
                    np.cos(latitude_rad)
                )

                dx = src.res[0] * meters_per_degree_lon
                dy = src.res[1] * meters_per_degree_lat

                # Calculate gradients
                gradient_y, gradient_x = np.gradient(
                    elevation,
                    dy,
                    dx
                )

                # Center pixel slope
                center_slope = np.sqrt(
                    gradient_x[1, 1] ** 2 +
                    gradient_y[1, 1] ** 2
                )

                slope_degrees = np.degrees(
                    np.arctan(center_slope)
                )

                if np.isfinite(slope_degrees):

                    df.at[
                        index,
                        "Slope_degrees"
                    ] = float(slope_degrees)

            except Exception:
                continue

            # Progress
            if (count + 1) % 500 == 0:

                print(
                    f"Processed {count + 1}/"
                    f"{len(inside_indices)} points"
                )


# ==========================================
# 5. Save dataset
# ==========================================

output_file = "data/ner_terrain_features.csv"

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 6. Statistics
# ==========================================

total = len(df)

found = df[
    "Slope_degrees"
].notna().sum()

missing = total - found


print("\n===================================")
print("SLOPE CALCULATION COMPLETE")
print("===================================")

print("Total landslides:", total)
print("Slope found:", found)
print("Slope missing:", missing)

print(
    "Coverage:",
    round(
        found / total * 100,
        2
    ),
    "%"
)

print("\nSlope statistics:")

print(
    df["Slope_degrees"].describe()
)

print("\nSaved to:")
print(output_file)