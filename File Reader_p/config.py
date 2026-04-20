import os

# ─────────────────────────────────────────────
# AWS / S3
# ─────────────────────────────────────────────
BUCKET_NAME      = os.environ.get("BUCKET_NAME",      "universal-file-reader-keerthana")
REGION           = os.environ.get("AWS_REGION",       "ap-south-1")

RAW_PREFIX       = os.environ.get("RAW_PREFIX",       "raw/")
PROCESSED_PREFIX = os.environ.get("PROCESSED_PREFIX", "processed/")
FAILED_PREFIX    = os.environ.get("FAILED_PREFIX",    "failed/")

# ─────────────────────────────────────────────
# SFTP
# ─────────────────────────────────────────────
SFTP_HOST     = os.environ.get("SFTP_HOST",     "localhost")
SFTP_PORT     = int(os.environ.get("SFTP_PORT", "22"))
SFTP_USERNAME = os.environ.get("SFTP_USERNAME", "")
SFTP_PASSWORD = os.environ.get("SFTP_PASSWORD", "")
SFTP_DIR      = os.environ.get("SFTP_DIR",      "/sftp-files")

# ─────────────────────────────────────────────
# Storage backend: "local" | "s3"
# ─────────────────────────────────────────────
STORAGE_TYPE   = os.environ.get("STORAGE_TYPE",   "local")
LOCAL_BASE_DIR = os.environ.get("LOCAL_BASE_DIR", ".")

# ─────────────────────────────────────────────
# Input path  – where raw files land locally
# ─────────────────────────────────────────────
INPUT_DIR = os.environ.get("INPUT_DIR", "raw")

# ─────────────────────────────────────────────
# Processing
# ─────────────────────────────────────────────
SUPPORTED_FILE_TYPES = ["csv", "txt", "xml", "pdf"]
PROCESSING_MODE      = os.environ.get("PROCESSING_MODE", "standard")  # standard | fast
FAST_MODE_LIMIT      = int(os.environ.get("FAST_MODE_LIMIT", "10"))

# ─────────────────────────────────────────────
# Output path – where processed JSON files land
# ─────────────────────────────────────────────
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "processed")
