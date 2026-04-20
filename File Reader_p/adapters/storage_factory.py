"""
adapters/storage_factory.py
----------------------------
Returns the right (upload_file, download_file) pair
based on STORAGE_TYPE from config.
"""

from config import STORAGE_TYPE


def get_storage():
    if STORAGE_TYPE == "s3":
        from adapters.s3_handler import upload_file, download_file
    elif STORAGE_TYPE == "local":
        from adapters.local_handler import upload_file, download_file
    else:
        raise ValueError(
            f"Unknown STORAGE_TYPE: '{STORAGE_TYPE}'. "
            "Set STORAGE_TYPE=local or STORAGE_TYPE=s3 in your environment."
        )
    return upload_file, download_file
