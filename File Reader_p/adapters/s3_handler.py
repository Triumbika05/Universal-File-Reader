"""
adapters/s3_handler.py
-----------------------
Storage adapter for AWS S3.
Bucket and region are read from config (env vars).
"""

import os
import boto3

from config import BUCKET_NAME, REGION

s3 = boto3.client("s3", region_name=REGION)


def upload_file(src: str, dest: str) -> str:
    """
    Upload local file src  →  s3://BUCKET_NAME/dest.
    Returns the S3 URI.
    """
    s3.upload_file(src, BUCKET_NAME, dest)
    s3_uri = f"s3://{BUCKET_NAME}/{dest}"
    print(f"  [s3] Stored : {os.path.abspath(src)}")
    print(f"       → {s3_uri}")
    return s3_uri


def download_file(src: str, dest: str) -> str:
    """
    Download s3://BUCKET_NAME/src  →  local dest.
    Returns the local path.
    """
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    s3.download_file(BUCKET_NAME, src, dest)
    print(f"  [s3] Fetched: s3://{BUCKET_NAME}/{src}")
    print(f"       → {os.path.abspath(dest)}")
    return dest
