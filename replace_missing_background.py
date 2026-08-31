import pandas as pd
import numpy as np
import rasterio
import glob


# ==========================================
# Load dataset
# ==========================================

file = "data/ml_terrain_dataset.csv"

df = pd.read_csv(file)

missing = df[
    (df["Label"] == 0) &
    (df["Elevation_m"].isna())
].copy()

valid = df[
    ~(
        (df["Label"] == 0) &
        (df["Elevation_m"].isna())
    )
].copy()

print("Missing background points:", len(missing))
print("Valid samples:", len(valid))


# ==========================================
# Find DEM coverage
# ==========================================

dem_files = glob.glob("data/dem*/*.tif")

coverage = []

for file in dem_files:

    with rasterio.open(file) as src:

        coverage.append({
            "left": src.bounds.left,
            "right": src.bounds.right,
            "bottom": src.bounds.bottom,
            "top": src.bounds.top
        })


# ==========================================
# Generate replacement points
# ==========================================

np.random.seed(123)

needed = len(missing)

new_points = []

print("\nGenerating replacement points...")


while len(new_points) < needed:

    lat = np.random.uniform(22.05, 28.96)
    lon = np.random.uniform(88.08, 96.62)

    # Check DEM coverage
    covered = False

    for b in coverage:

        if (
            b["left"] <= lon <= b["right"]
            and
            b["bottom"] <= lat <= b["top"]
        ):
            covered = True
            break

    if not covered:
        continue

    # Check distance from known landslides
    distances = (
        (valid[valid["Label"] == 1]["Latitude"] - lat) ** 2
        +
        (valid[valid["Label"] == 1]["Longitude"] - lon) ** 2
    )

    if len(distances) > 0 and distances.min() < 0.0005:
        continue

    new_points.append({
        "Latitude": lat,
        "Longitude": lon,
        "Elevation_m": np.nan,
        "Slope_degrees": np.nan,
        "Label": 0
    })


replacement = pd.DataFrame(new_points)

print("Replacement points:", len(replacement))


# ==========================================
# Combine
# ==========================================

final = pd.concat(
    [
        valid,
        replacement
    ],
    ignore_index=True
)


# ==========================================
# Save
# ==========================================

output = "data/ml_terrain_dataset_clean.csv"

final.to_csv(
    output,
    index=False
)

print("\n===================================")
print("REPLACEMENT POINTS CREATED")
print("===================================")

print("Total samples:", len(final))
print("Landslides:", (final["Label"] == 1).sum())
print("Background:", (final["Label"] == 0).sum())

print("\nSaved to:")
print(output)