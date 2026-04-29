import os
import shutil
from ingestion.input_handler import fetch_input
from storage.output_handler import save_output
from parsers.parser_factory import get_parser
from config.config import Config


def process(input_value):
    try:
        file_path = fetch_input(input_value)

        file_type = file_path.split(".")[-1].lower()

        if file_type not in Config.PROCESSING["supported_types"]:
            raise Exception(f"Unsupported file type: {file_type}")

        parser = get_parser(file_type)

        result = parser(file_path)

        # ✅ ONLY SAVE IF SUCCESS
        if "schema" in result:
            save_output(result)

        return [result]

    except Exception as e:
        # Handle failed files
        if file_path.startswith(Config.TEMP_DIR):
            os.remove(file_path)
        else:
            failed_dir = "data/failed"
            os.makedirs(failed_dir, exist_ok=True)
            shutil.move(file_path, os.path.join(failed_dir, os.path.basename(file_path)))

        return [{ 
            "file": input_value,
            "status": "failed",
            "error": str(e)
        }]









