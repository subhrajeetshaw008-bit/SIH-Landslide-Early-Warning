import pandas as pd
import folium

# Load NER landslide data
df = pd.read_csv("data/ner_landslides.csv")

# Create map centered on Northeast India
m = folium.Map(
    location=[25.2, 93.05],
    zoom_start=6
)

# Add landslide points
for _, row in df.iterrows():

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=2,
        popup=(
            f"State: {row['State']}<br>"
            f"District: {row['District']}<br>"
            f"Type: {row['Movement_Type']}"
        ),
        fill=True
    ).add_to(m)

# Save map
output_file = "data/ner_landslide_map.html"

m.save(output_file)

print("Map created successfully!")
print(f"Saved to: {output_file}")
print(f"Total points: {len(df)}")