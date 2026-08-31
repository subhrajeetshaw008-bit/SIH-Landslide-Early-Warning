import pandas as pd

# Input file
input_file = "data/landslide_raw.csv"

# Output file
output_file = "data/ner_landslides.csv"

# NER states
ner_states = [
    "Arunachal Pradesh",
    "Assam",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Sikkim",
    "Tripura"
]

print("Loading GSI landslide data...")

# Read without assuming headers
df = pd.read_csv(input_file, header=None)

# Assign correct column names
df.columns = [
    "Sl_No",
    "Slide_No",
    "State",
    "District",
    "Slide_Name",
    "NH_SH_Location",
    "Latitude",
    "Longitude",
    "Material_Involved",
    "Movement_Type",
    "History"
]

# Remove the title/header rows accidentally extracted from PDF
df = df[df["State"].isin(ner_states)].copy()

# Clean text columns
for column in [
    "State",
    "District",
    "Slide_Name",
    "NH_SH_Location",
    "Material_Involved",
    "Movement_Type"
]:
    df[column] = df[column].astype(str).str.strip()

# Convert coordinates to numbers
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# Remove rows without valid coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Keep realistic geographic coordinates
df = df[
    (df["Latitude"] >= 20) &
    (df["Latitude"] <= 30) &
    (df["Longitude"] >= 88) &
    (df["Longitude"] <= 98)
]

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("\n================================")
print("NER DATASET CREATED SUCCESSFULLY")
print("================================")

print(f"\nTotal NER landslides: {len(df)}")

print("\nLandslides by state:")
print(df["State"].value_counts().to_string())

print("\nColumns:")
print(df.columns.tolist())

print(f"\nSaved to:")
print(output_file)