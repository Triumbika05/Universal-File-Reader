"""
adapters/sftp_ingestor.py
--------------------------
Downloads all files from the configured SFTP directory
and uploads them to S3 under RAW_PREFIX.

All connection details come from config (env vars) — nothing hardcoded.
"""

import os
import paramiko
import boto3

from config import (
    SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD, SFTP_DIR,
    BUCKET_NAME, RAW_PREFIX, REGION,
)

s3 = boto3.client("s3", region_name=REGION)


def fetch_from_sftp() -> list:
    """
    Connect to SFTP, download every file in SFTP_DIR, upload each to S3.
    Returns a list of S3 keys that were created.
    """
    print(f"\n🔌 Connecting to SFTP  {SFTP_HOST}:{SFTP_PORT}  dir={SFTP_DIR}")

    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.chdir(SFTP_DIR)

    files = sftp.listdir()
    print(f"   Files found : {files}")

    uploaded_keys = []
    for file in files:
        local_path = os.path.join("/tmp", file)
        s3_key     = f"{RAW_PREFIX}{file}"

        print(f"  ↓ Downloading {file}  →  {local_path}")
        sftp.get(file, local_path)

        print(f"  ↑ Uploading   {local_path}  →  s3://{BUCKET_NAME}/{s3_key}")
        s3.upload_file(local_path, BUCKET_NAME, s3_key)

        uploaded_keys.append(s3_key)

    sftp.close()
    transport.close()
    print(f"✅ SFTP ingestion complete — {len(files)} file(s) uploaded to s3://{BUCKET_NAME}/{RAW_PREFIX}\n")
    return uploaded_keys


if __name__ == "__main__":
    fetch_from_sftp()
