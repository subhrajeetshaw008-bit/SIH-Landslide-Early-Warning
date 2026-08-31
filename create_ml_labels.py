import pandas as pd
import numpy as np


# ==========================================
# 1. Load real landslide locations
# ==========================================

input_file = "data/ner_terrain_features.csv"

landslides = pd.read_csv(input_file)

print("Real landslides:", len(landslides))


# ==========================================
# 2. Add positive label
# ==========================================

landslides["Label"] = 1


# ==========================================
# 3. Define NER geographic bounds
# ==========================================

LAT_MIN = 22.0
LAT_MAX = 29.1

LON_MIN = 88.0
LON_MAX = 96.8


# ==========================================
# 4. Generate background points
# ==========================================

np.random.seed(42)

target_points = len(landslides)

background = []

print("\nGenerating background points...")

while len(background) < target_points:

    latitude = np.random.uniform(
        LAT_MIN,
        LAT_MAX
    )

    longitude = np.random.uniform(
        LON_MIN,
        LON_MAX
    )

    # Check distance from known landslides
    distances = (
        (landslides["Latitude"] - latitude) ** 2
        +
        (landslides["Longitude"] - longitude) ** 2
    )

    # Reject points too close to known landslides
    if distances.min() > 0.0005:

        background.append(
            {
                "Latitude": latitude,
                "Longitude": longitude,
                "Label": 0
            }
        )


background = pd.DataFrame(background)

print(
    "Background points created:",
    len(background)
)


# ==========================================
# 5. Combine datasets
# ==========================================

landslides = landslides[
    [
        "Latitude",
        "Longitude",
        "Elevation_m",
        "Slope_degrees",
        "Label"
    ]
]

background = background[
    [
        "Latitude",
        "Longitude",
        "Label"
    ]
]


dataset = pd.concat(
    [
        landslides,
        background
    ],
    ignore_index=True
)


# ==========================================
# 6. Save
# ==========================================

output_file = "data/ml_base_dataset.csv"

dataset.to_csv(
    output_file,
    index=False
)


# ==========================================
# 7. Report
# ==========================================

print("\n===================================")
print("ML BASE DATASET CREATED")
print("===================================")

print("Total samples:", len(dataset))

print("\nLabels:")
print(
    dataset["Label"]
    .value_counts()
    .sort_index()
)

print("\nSaved to:")
print(output_file)