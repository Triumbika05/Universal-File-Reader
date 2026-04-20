"""
triggers/lambda_handler.py
--------------------------
AWS Lambda trigger — fires when a file is PUT into S3 under RAW_PREFIX.

Event source : S3 → Put Object notification (raw/ prefix)

Flow:
    S3 raw/file  →  download to /tmp  →  process  →  upload to S3 processed/
"""

import os

from core.pipeline import run_pipeline
from adapters.s3_handler import download_file, upload_file
from config import PROCESSED_PREFIX, FAILED_PREFIX


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key    = record["s3"]["object"]["key"]

    file_name  = os.path.basename(key)
    local_path = f"/tmp/{file_name}"

    print(f"\n📥 Triggered by : s3://{bucket}/{key}")
    print(f"   Local tmp    : {local_path}")

    try:
        # Step 1 – Download raw file from S3 to Lambda /tmp
        download_file(key, local_path)

        # Step 2 – Process
        result = run_pipeline(local_path)

        # Step 3 – Upload processed JSON back to S3
        output_name    = os.path.basename(result["output_file"])
        processed_dest = upload_file(result["output_file"], f"{PROCESSED_PREFIX}{output_name}")

        print(f"\n✅ Lambda completed")
        print(f"   Input  : s3://{bucket}/{key}")
        print(f"   Output : {processed_dest}")

        return {
            "status":        "success",
            "input_s3_key":  key,
            "input_path":    result["input_path"],
            "output_file":   result["output_file"],
            "processed_at":  str(processed_dest),
            "total_records": result["total_records"],
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        # Move failed file to failed/ prefix so it can be inspected
        upload_file(local_path, f"{FAILED_PREFIX}{file_name}")
        raise
