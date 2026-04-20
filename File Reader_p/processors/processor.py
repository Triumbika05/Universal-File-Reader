"""
processors/processor.py
-----------------------
Detects file type, parses the file, and writes a JSON output.

All paths are driven by config:
  - INPUT_DIR  : where raw input files are expected
  - OUTPUT_DIR : where _output.json files are written
"""

import csv
import json
import os
import xml.etree.ElementTree as ET

from PyPDF2 import PdfReader

from config import (
    SUPPORTED_FILE_TYPES,
    PROCESSING_MODE,
    FAST_MODE_LIMIT,
    INPUT_DIR,
    OUTPUT_DIR,
)


# ─────────────────────────────────────────────
# Detect file type from extension
# ─────────────────────────────────────────────
def detect_file_type(file_name: str) -> str:
    ext = os.path.splitext(file_name)[-1].lower().lstrip(".")
    return ext if ext in SUPPORTED_FILE_TYPES else "unknown"


# ─────────────────────────────────────────────
# Resolve the full input path from INPUT_DIR
# ─────────────────────────────────────────────
def resolve_input_path(file_name: str) -> str:
    """
    If file_name already contains a directory component, use it as-is.
    Otherwise look it up under INPUT_DIR.
    """
    if os.path.dirname(file_name):          # path was given explicitly
        return file_name
    candidate = os.path.join(INPUT_DIR, file_name)
    if os.path.exists(candidate):
        return candidate
    return file_name                        # fall back to cwd


# ─────────────────────────────────────────────
# Parsers
# ─────────────────────────────────────────────
def process_csv(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def process_txt(file_path: str) -> list:
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                data.append({"name": parts[0], "age": parts[1], "city": parts[2]})
    return data


def process_xml(file_path: str) -> list:
    data = []
    root = ET.parse(file_path).getroot()
    for emp in root.findall("employee"):
        record = {child.tag: child.text for child in emp}
        data.append(record)
    return data


def process_pdf(file_path: str) -> list:
    data = []
    for page_num, page in enumerate(PdfReader(file_path).pages, start=1):
        text = page.extract_text() or ""
        for line in text.split("\n"):
            line = line.strip()
            if line:
                data.append({"page": page_num, "content": line})
    return data


PROCESSOR_MAP = {
    "csv": process_csv,
    "txt": process_txt,
    "xml": process_xml,
    "pdf": process_pdf,
}


# ─────────────────────────────────────────────
# Write JSON output
# ─────────────────────────────────────────────
def create_output(file_path: str, data: list) -> str:
    """
    Write processed data to OUTPUT_DIR/<basename>_output.json.
    Returns the full path of the output file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base_name   = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(OUTPUT_DIR, f"{base_name}_output.json")

    payload = {
        "source_file":  os.path.abspath(file_path),
        "input_dir":    os.path.abspath(INPUT_DIR),
        "output_dir":   os.path.abspath(OUTPUT_DIR),
        "output_file":  os.path.abspath(output_file),
        "total_records": len(data),
        "data":         data,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(f"  Input  path : {os.path.abspath(file_path)}")
    print(f"  Output path : {os.path.abspath(output_file)}")

    return output_file


# ─────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────
def main(file_name: str):
    file_path = resolve_input_path(file_name)
    file_type = detect_file_type(file_path)

    if file_type not in SUPPORTED_FILE_TYPES:
        print(f"❌ Unsupported file type: '{file_type}'")
        return

    print(f"\n📂 Input  : {os.path.abspath(file_path)}")

    data = PROCESSOR_MAP[file_type](file_path)

    if PROCESSING_MODE == "fast":
        data = data[:FAST_MODE_LIMIT]

    output_file = create_output(file_path, data)
    print(f"📁 Output : {os.path.abspath(output_file)}\n")
