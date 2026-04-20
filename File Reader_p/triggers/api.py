"""
triggers/api.py
---------------
FastAPI HTTP trigger for the pipeline.

Start:
    uvicorn triggers.api:app --reload

Endpoint:
    POST /process?file_path=employee_data.csv

Response:
    {
        "status":        "success",
        "input_path":    "/abs/path/to/employee_data.csv",
        "input_dir":     "/abs/path/to/raw",
        "raw_stored_at": "raw/employee_data.csv",
        "output_file":   "/abs/path/to/processed/employee_data_output.json",
        "output_dir":    "/abs/path/to/processed",
        "processed_at":  "processed/employee_data_output.json",
        "total_records": 100,
        "message":       "Processed 100 records from 'employee_data.csv'"
    }
"""

import os
from fastapi import FastAPI, HTTPException

from core.pipeline import run_pipeline
from adapters.storage_factory import get_storage
from config import RAW_PREFIX, PROCESSED_PREFIX

app = FastAPI(title="Universal File Reader API")

upload_file, download_file = get_storage()


@app.post("/process")
def process_file(file_path: str):
    try:
        file_name = os.path.basename(file_path)

        # Step 1 – Store raw input
        raw_dest = upload_file(file_path, f"{RAW_PREFIX}{file_name}")

        # Step 2 – Process
        result = run_pipeline(file_path)

        # Step 3 – Store processed output
        output_name    = os.path.basename(result["output_file"])
        processed_dest = upload_file(result["output_file"], f"{PROCESSED_PREFIX}{output_name}")

        return {
            "status":        "success",
            "input_path":    result["input_path"],
            "input_dir":     result["input_dir"],
            "raw_stored_at": str(raw_dest),
            "output_file":   result["output_file"],
            "output_dir":    result["output_dir"],
            "processed_at":  str(processed_dest),
            "total_records": result["total_records"],
            "message":       result["message"],
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
