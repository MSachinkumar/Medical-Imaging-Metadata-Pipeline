import os
from pathlib import Path

import pandas as pd
import pydicom
from tqdm import tqdm

# -------------------------------
# Project Paths
# -------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DICOM_DIR = PROJECT_ROOT / "data" / "raw_dicom" / "lidc_idri"

OUTPUT_DIR = PROJECT_ROOT / "processed"

OUTPUT_FILE = OUTPUT_DIR / "metadata_raw.csv"

# -------------------------------
# Find all DICOM files
# -------------------------------

dicom_files = list(RAW_DICOM_DIR.rglob("*.dcm"))

print(f"Found {len(dicom_files)} DICOM files.")


# -------------------------------
# Extract metadata from all DICOM files
# -------------------------------

from pydicom.errors import InvalidDicomError

metadata = []
failed_files = []

for dicom_file in tqdm(dicom_files):
    try:
        ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)

    except InvalidDicomError:
        try:
            # Try reading non-standard DICOM
            ds = pydicom.dcmread(
                dicom_file,
                stop_before_pixels=True,
                force=True
            )
        except Exception as e:
            failed_files.append({
                "file_path": str(dicom_file),
                "error": str(e)
            })
            continue

    except Exception as e:
        failed_files.append({
            "file_path": str(dicom_file),
            "error": str(e)
        })
        continue

    metadata.append({
        "patient_id": ds.get("PatientID"),
        "study_uid": ds.get("StudyInstanceUID"),
        "series_uid": ds.get("SeriesInstanceUID"),
        "sop_instance_uid": ds.get("SOPInstanceUID"),
        "modality": ds.get("Modality"),
        "manufacturer": ds.get("Manufacturer"),
        "rows": ds.get("Rows"),
        "columns": ds.get("Columns"),
        "slice_thickness": ds.get("SliceThickness"),
        "pixel_spacing": str(ds.get("PixelSpacing")),
        "file_path": str(dicom_file)
    })


# -------------------------------
# Convert to DataFrame
# -------------------------------

df = pd.DataFrame(metadata)

# Remove duplicate DICOM instances
df = df.drop_duplicates(subset=["sop_instance_uid"])

print(df.head())

print(f"\nUnique metadata records : {len(df)}")
print(f"Failed files            : {len(failed_files)}")

# -------------------------------
# Create output directory
# -------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Save metadata to CSV
# -------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nMetadata saved to:\n{OUTPUT_FILE}")

# -------------------------------
# Create output directory
# -------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Save metadata to CSV
# -------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nMetadata saved to:\n{OUTPUT_FILE}")

