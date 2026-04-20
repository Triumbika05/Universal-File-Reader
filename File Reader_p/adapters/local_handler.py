"""
adapters/local_handler.py
--------------------------
Storage adapter for local filesystem.
Uses LOCAL_BASE_DIR as the root for all uploads/downloads.
"""

import os
import shutil

from config import LOCAL_BASE_DIR


def upload_file(src: str, dest: str) -> str:
    """
    Copy src  →  LOCAL_BASE_DIR/dest.
    Returns the full destination path.
    """
    full_dest = os.path.join(LOCAL_BASE_DIR, dest)
    os.makedirs(os.path.dirname(os.path.abspath(full_dest)), exist_ok=True)
    shutil.copy(src, full_dest)
    print(f"  [local] Stored : {os.path.abspath(src)}")
    print(f"          → {os.path.abspath(full_dest)}")
    return full_dest


def download_file(src: str, dest: str) -> str:
    """
    Copy LOCAL_BASE_DIR/src  →  dest.
    Returns the full destination path.
    """
    full_src = os.path.join(LOCAL_BASE_DIR, src)
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    shutil.copy(full_src, dest)
    print(f"  [local] Fetched: {os.path.abspath(full_src)}")
    print(f"          → {os.path.abspath(dest)}")
    return dest
