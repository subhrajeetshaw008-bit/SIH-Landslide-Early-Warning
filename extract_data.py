import pdfplumber
import pandas as pd
import os

pdf_path = "data/landslide_report.pdf"
output_path = "data/landslide_raw.csv"

all_rows = []

print("Starting PDF extraction...")
print("This may take several minutes for 904 pages.\n")

with pdfplumber.open(pdf_path) as pdf:

    total_pages = len(pdf.pages)

    for page_number, page in enumerate(pdf.pages, start=1):

        try:
            tables = page.extract_tables()

            for table in tables:

                if table:
                    for row in table:
                        if row and any(cell for cell in row):
                            all_rows.append(row)

            if page_number % 25 == 0:
                print(
                    f"Processed {page_number}/{total_pages} pages..."
                )

        except Exception as e:
            print(f"Error on page {page_number}: {e}")

print("\nExtraction finished.")

if all_rows:

    df = pd.DataFrame(all_rows)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    df.to_csv(output_path, index=False)

    print(f"\nSaved extracted data to:")
    print(output_path)

    print(f"\nRows extracted: {len(df)}")
    print(f"Columns detected: {len(df.columns)}")

else:
    print("No tables were extracted.")