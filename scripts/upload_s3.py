import os

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

print(AWS_REGION)
print(BUCKET_NAME)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

print("Connected to S3 client successfully!")

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "processed" / "metadata_clean.csv"

print(CSV_FILE)

print("Uploading file to S3...")

s3_client.upload_file(
    str(CSV_FILE),          # Local file on your computer
    BUCKET_NAME,            # S3 bucket name
    "metadata/metadata_clean.csv"   # Object name inside the bucket
)

print("Upload completed!")