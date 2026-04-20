"""
core/pipeline.py
----------------
Orchestrates the full flow:
  1. Resolve input path  (INPUT_DIR / file)
  2. Detect file type
  3. Parse file
  4. Write output to OUTPUT_DIR
  5. Return a result dict with every path clearly listed
"""

import os

from config import SUPPORTED_FILE_TYPES, PROCESSING_MODE, FAST_MODE_LIMIT, INPUT_DIR, OUTPUT_DIR
from processors.processor import (
    PROCESSOR_MAP,
    detect_file_type,
    resolve_input_path,
    create_output,
)


def run_pipeline(file_path: str) -> dict:
    """
    Run the full pipeline for a given file.

    Returns a result dict:
        {
            "status":        "success" | "error",
            "input_path":    absolute path of the source file,
            "input_dir":     configured INPUT_DIR,
            "output_file":   absolute path of the JSON output,
            "output_dir":    configured OUTPUT_DIR,
            "total_records": int,
            "message":       human-readable summary,
        }
    """
    resolved = resolve_input_path(file_path)

    print(f"\n🚀 Pipeline started")
    print(f"   Input  dir  : {os.path.abspath(INPUT_DIR)}")
    print(f"   Output dir  : {os.path.abspath(OUTPUT_DIR)}")
    print(f"   File        : {os.path.abspath(resolved)}")

    file_type = detect_file_type(resolved)

    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(
            f"Unsupported file type: '{file_type}'. "
            f"Supported: {SUPPORTED_FILE_TYPES}"
        )

    data = PROCESSOR_MAP[file_type](resolved)

    if PROCESSING_MODE == "fast":
        data = data[:FAST_MODE_LIMIT]

    output_file = create_output(resolved, data)

    result = {
        "status":        "success",
        "input_path":    os.path.abspath(resolved),
        "input_dir":     os.path.abspath(INPUT_DIR),
        "output_file":   os.path.abspath(output_file),
        "output_dir":    os.path.abspath(OUTPUT_DIR),
        "total_records": len(data),
        "message":       f"Processed {len(data)} records from '{os.path.basename(resolved)}'",
    }

    print(f"\n✅ Pipeline completed")
    print(f"   Records     : {len(data)}")
    print(f"   Output file : {os.path.abspath(output_file)}\n")

    return result
