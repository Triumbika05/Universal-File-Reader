"""
triggers/cli.py
---------------
Command-line trigger for the pipeline.

Usage:
    python -m triggers.cli <file_path>

Examples:
    python -m triggers.cli employee_data.csv
    python -m triggers.cli raw/data.xml

What it does:
    1. Copies / uploads the raw input file  →  INPUT_DIR  (or RAW_PREFIX on S3)
    2. Runs the pipeline                    →  OUTPUT_DIR
    3. Copies / uploads the output JSON     →  PROCESSED_PREFIX
    4. Prints a full path summary
"""

import sys
import os

from core.pipeline import run_pipeline
from adapters.storage_factory import get_storage
from config import RAW_PREFIX, PROCESSED_PREFIX, INPUT_DIR, OUTPUT_DIR

upload_file, download_file = get_storage()


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m triggers.cli <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)

    print("\n─────────────────────────────────────────")
    print("  Universal File Reader  —  CLI Trigger")
    print("─────────────────────────────────────────")

    # Step 1 – Store raw input
    print(f"\n[1/3] Storing raw input ...")
    raw_dest = upload_file(file_path, f"{RAW_PREFIX}{file_name}")

    # Step 2 – Process
    print(f"\n[2/3] Processing ...")
    result = run_pipeline(file_path)

    # Step 3 – Store processed output
    print(f"\n[3/3] Storing processed output ...")
    output_name = os.path.basename(result["output_file"])
    processed_dest = upload_file(result["output_file"], f"{PROCESSED_PREFIX}{output_name}")

    # Summary
    print("\n─────────────────────────────────────────")
    print("  ✅ Pipeline Summary")
    print("─────────────────────────────────────────")
    print(f"  Source file    : {result['input_path']}")
    print(f"  Raw stored at  : {raw_dest}")
    print(f"  Input dir      : {result['input_dir']}")
    print(f"  Output dir     : {result['output_dir']}")
    print(f"  Output file    : {result['output_file']}")
    print(f"  Processed at   : {processed_dest}")
    print(f"  Total records  : {result['total_records']}")
    print("─────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
