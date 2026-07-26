from pathlib import Path

import pandas as pd
import psycopg2

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "processed" / "metadata_clean.csv"

try:
    conn = psycopg2.connect(
        host="localhost",
        database="medical_imaging",
        user="sachin",
        password="YOUR_POSTGRES_PASSWORD",  # Replace with your password
        port=5432
    )

    print("✅ Connected to PostgreSQL!")

    cursor = conn.cursor()

    # Read cleaned metadata
    df = pd.read_csv(CSV_FILE)

    print(f"Loaded {len(df)} records from CSV.")

    duplicates = df[df.duplicated(subset=["sop_instance_uid"], keep=False)]

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.width", None)

    print(duplicates[
        [
            "patient_id",
            "study_uid",
            "series_uid",
            "sop_instance_uid",
            "file_path"
        ]
    ].head(20).to_string(index=False))

    counts = df["sop_instance_uid"].value_counts()

    print("\nMost repeated SOP Instance UIDs:")
    print(counts.head(10))

    uid = counts.index[0]

    print("\nFiles having this UID:\n")

    print(
        df[df["sop_instance_uid"] == uid][
            ["file_path", "patient_id"]
        ].to_string(index=False)
    )

    # Extract unique patients
    patients = (
        df[["patient_id"]]
        .drop_duplicates()
        .dropna()
    )

    # Insert patients
    for _, row in patients.iterrows():
        cursor.execute(
            """
            INSERT INTO metadata.patients (patient_id)
            VALUES (%s)
            ON CONFLICT (patient_id) DO NOTHING;
            """,
            (row["patient_id"],)
        )

    conn.commit()

    print(f"Inserted {len(patients)} patients.")


    studies = (
        df[["study_uid", "patient_id"]]
        .drop_duplicates()
        .dropna()
    )

    for _, row in studies.iterrows():
        cursor.execute(
            """
            INSERT INTO metadata.studies (study_uid, patient_id)
            VALUES (%s, %s)
            ON CONFLICT (study_uid) DO NOTHING;
            """,
            (
                row["study_uid"],
                row["patient_id"]
            )
        )

    conn.commit()

    print(f"Inserted {len(studies)} studies.")

    series = (
        df[["series_uid", "study_uid", "modality"]]
        .drop_duplicates()
        .dropna()
    )

    for _, row in series.iterrows():
        cursor.execute(
            """
            INSERT INTO metadata.series (
                series_uid,
                study_uid,
                modality
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (series_uid) DO NOTHING;
            """,
            (
                row["series_uid"],
                row["study_uid"],
                row["modality"]
            )
        )

    conn.commit()

    print(f"Inserted {len(series)} series.")

    images = (
        df[
            [
                "sop_instance_uid",
                "series_uid",
                "manufacturer",
                "rows",
                "columns",
                "slice_thickness",
                "pixel_spacing",
                "file_path"
            ]
        ]
        .drop_duplicates()
        .dropna(subset=["sop_instance_uid", "series_uid"])
    )

    for _, row in images.iterrows():
        cursor.execute(
            """
            INSERT INTO metadata.images (
                sop_instance_uid,
                series_uid,
                manufacturer,
                rows,
                columns,
                slice_thickness,
                pixel_spacing,
                file_path
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sop_instance_uid) DO NOTHING;
            """,
            (
                row["sop_instance_uid"],
                row["series_uid"],
                row["manufacturer"],
                int(row["rows"]) if pd.notna(row["rows"]) else None,
                int(row["columns"]) if pd.notna(row["columns"]) else None,
                row["slice_thickness"],
                row["pixel_spacing"],
                row["file_path"]
            )
        )

    conn.commit()

    print(f"Inserted {len(images)} images.")

    cursor.close()
    conn.close()

    print("Patients :", df["patient_id"].nunique())
    print("Studies  :", df["study_uid"].nunique())
    print("Series   :", df["series_uid"].nunique())
    print("Images   :", df["sop_instance_uid"].nunique())

except Exception as e:
    print("Connection failed:")
    print(e)