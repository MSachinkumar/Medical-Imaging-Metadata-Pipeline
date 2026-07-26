from pathlib import Path

import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "processed" / "metadata_raw.csv"

OUTPUT_FILE = PROJECT_ROOT / "processed" / "metadata_clean.csv"
df = pd.read_csv(INPUT_FILE)

print(df.head())
df = pd.read_csv(INPUT_FILE)
print("=" * 50)
print("Dataset Shape")
print("=" * 50)
print(df.shape)
print("\n" + "=" * 50)
print("Data Types")
print("=" * 50)

print(df.dtypes)
print("\n" + "=" * 50)
print("Missing Values")
print("=" * 50)

print(df.isnull().sum())
print("\n" + "=" * 50)
print("Duplicate Rows")
print("=" * 50)

print(df.duplicated().sum())
print("\n" + "=" * 50)
print("Summary Statistics")
print("=" * 50)

print(df.describe(include="all"))
print("\nRemoving rows with missing identifiers...")

df = df.dropna(
    subset=[
        "patient_id",
        "study_uid",
        "series_uid",
        "sop_instance_uid"
    ]
)

print(f"Rows remaining: {len(df)}")
numeric_columns = [
    "rows",
    "columns",
    "slice_thickness"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.drop_duplicates()
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nClean metadata saved to:\n{OUTPUT_FILE}")
